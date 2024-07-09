# 1 Для создания фотографии итерирует по словарю типа {photo_id1: photo1, ... , photo_id999: photo999} 
# 2 К каждой фотографии запускает функцию create_image_rgb
# 3 При помощи image_rgb создает гистограму фотографии 
# 3/1 Нормализовать гистограмы при помощи функции normilize_hist
# 4 Создает объект класса Photo и передает туда photo_id, histogram, link 
# 5 Записывает новый объект в словарь внутри DataStorage типа {photo_id1: Photo, ... , photo_id999: Photo}

import cv2
import io
import numpy as np

from data_storage import DataStorage
from photo import Photo

class EntityCreator:
      
    def __init__(self, data_storage: DataStorage, logger):
        self.data_storage = data_storage
        self.__logger = logger

    def simple_logger(func):
            
        def wrapper(self, *args, **kwargs):

                self.__logger.debug(f'Запускаем функцию {func.__name__}()')
                try:
                        result = func(self, *args, **kwargs)
                        return result

                except Exception as e:
                        self.__logger.exception(f"Ошибка в {func.__name__}():\n {e}")
        
        return wrapper


    @simple_logger
    def create_image_rgb(self, image_to_check: bytes):
        """Загружаем изображение в байтах, декодируем с помощью numpy, переводим в RGB и возвращаем"""

        self.__logger.debug('Выполняем загрузку изображения с последующим переводом в RGB формат')
        # image_stream = io.BytesIO(image_to_check)
        image_bgr = cv2.imdecode(np.frombuffer(image_to_check.read(), np.uint8), cv2.IMREAD_COLOR)
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

        return image_rgb


    @simple_logger
    def calculate_histogram(self, image_rgb):
        """Вычисление гистограммы изображения"""

        self.__logger.debug('Выполняем вычисление гистограммы')
        calculated_hist = cv2.calcHist([image_rgb], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])

        return calculated_hist


    @simple_logger
    def normilize_hist(self, calculated_hist):
        """Нормализация гистограммы, приведение значения гистограммы к единице"""
        
        self.__logger.debug('Выполняем функцию нормализации гистограммы')
        normilized_hist = calculated_hist / calculated_hist.sum()
        return normilized_hist

    
    @simple_logger
    def create_photo(self):
        #Условный фотодикт
        """Пока есть данные в photo_dict, на каждой итерации создаем изображение, вычисляем его гистограмму
         затем записываем в DataStorage и явно удаляем объект для освобождения памяти"""
        
        self.__logger.debug('Выполняем вычисление всех параметров объекта Photo с последующей записью в DataStorage')
        for photo_id, photo_data in self.data_storage.raw_photo_dict.items():
            image_bytes = photo_data['image_bytes']
            link = photo_data['link']

            image_rgb = self.create_image_rgb(image_bytes)

            histogram = self.calculate_histogram(image_rgb)

            normilized_histogram = self.normilize_hist(histogram)

            photo = Photo(photo_id, normilized_histogram, link)
            self.data_storage.photo_dict[photo_id] = photo

            del photo