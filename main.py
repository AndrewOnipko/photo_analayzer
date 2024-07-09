from photo_analayzer_test import PhotoAnalyzer
from data_storage import DataStorage
from entity_creator import EntityCreator
import logging
import os

def main():

    script_name = os.path.basename(__file__)
    file_directory = os.path.realpath(__file__).replace(f"/{script_name}", "")

    logging.basicConfig(format='%(asctime)s %(message)s',
                        level=logging.DEBUG,
                        filename=f"{file_directory}/logs.txt",
                        filemode='w') # Настройки логгирования

    logger = logging.getLogger() # Создание логгера 

    path1 = '/home/stoltz/Рабочий стол/new_folder/original.jpg'
    path2 = '/home/stoltz/Рабочий стол/new_folder/one_mark_middle.webp'
    equality_limit = 70

    data_storage = DataStorage()
    entity_creator = EntityCreator(data_storage, logger)
    photo_analayzer = PhotoAnalyzer(equality_limit, logger)

    raw_photo_1 = open(path1, 'rb')
    raw_photo_2 = open(path2, 'rb')

    raw_photo_list = [raw_photo_1, raw_photo_2]

    for photo_id in range(1,3):
        data_storage.raw_photo_dict[photo_id] = {}
        data_storage.raw_photo_dict[photo_id] = {'image_bytes':raw_photo_list[photo_id - 1],'link':'test_link'}

    entity_creator.create_photo()

    photo_1 = data_storage.photo_dict[1]
    photo_2 = data_storage.photo_dict[2]

    result = photo_analayzer.photo_comperison(photo_1, photo_2)
    print(result)


if __name__ == '__main__':
    main()