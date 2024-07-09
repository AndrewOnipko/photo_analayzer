import cv2

from photo import Photo

class PhotoAnalyzer:
    
    def __init__(self, equality_limit: int, logger):
        self.__equality_limit = equality_limit
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
    def set_equality_limit(self, new_equality_limit):
        """ Меняем допустимый порог совпадений """

        self.__logger.debug('Запускаем функцию изменения значения допустимого лимита совпадений')
        self.__equality_limit = new_equality_limit


    @simple_logger
    def get_equality_limit(self):
        """Возвращаем значение допустимого порога совпадений"""

        self.__logger.debug('Возвращаем допустимый лимит совпадений')
        return self.__equality_limit


    @simple_logger
    def photo_comperison(self, photo_1: Photo, photo_2: Photo):
        """///"""

        self.__logger.debug('Выполнение функции сравнения двух гистограмм фотографий и сравнение их с допустимым порогом совпадений')
        calculated_correlation_percent = self.calculate_correlation_percent(photo_1, photo_2)
        is_simmular = self.is_simmular(calculated_correlation_percent)
        return is_simmular


    @simple_logger
    def calculate_correlation_percent(self, photo_1, photo_2):
        """Вычисление корреляции между гистограммами"""

        self.__logger.debug('Выполнение функции поиска корреляции между двумя гистограммами')
        correlation_float = cv2.compareHist(photo_1.histogram, photo_2.histogram, cv2.HISTCMP_CORREL)
        correlation_percent = correlation_float * 100
        
        return correlation_percent
    

    @simple_logger
    def is_simmular(self, correlation_percent):
        """Проверяем, меньше ли результат кореляции гистограм допустимого лимита"""

        self.__logger.debug('Выполнения функции сравнения итогового результата кореляции с допустимым лимитом')
        if correlation_percent > self.__equality_limit:
            return True
        else:
            return False