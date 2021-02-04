"""
    Модуль для парсинга файла
"""
import csv
import json
import xml.etree.ElementTree as ElementTree
import os.path as path


def exist_file(file_path):
    """Выполняет проверку на существование файла по указанному пути.

      Входное значение file_path - путь к файлу

      Возвращает логическое значение.
    """
    if not path.exists(file_path):
        print("No such file or directory: '%s'" % file_path)
        return False
    return True


def parse_csv(file_path):
    """Парсит файл формата .csv по указанному пути.

          Входное значение file_path - путь к файлу

          Возвращает список из словарей в которых, ключ - название столбца из файла
    """
    with open(file_path, newline='') as csv_file:
        file_data = csv.reader(csv_file)
        columns_name = next(file_data)
        result_parse = []
        for row in file_data:
            new_dict = dict.fromkeys(columns_name)
            for key, item in zip(new_dict, row):
                new_dict[key] = item
            else:
                result_parse.append(new_dict)
        print("Файл '%s' успешно обработан" % file_path)
    return result_parse


def parse_json(file_path):
    """Парсит файл формата .json по указанному пути.

             Входное значение file_path - путь к файлу

             Возвращает список из словарей в которых, ключ - название поле из json-объкекта
    """
    with open(file_path) as json_file:
        result_parse = json.load(json_file)['fields']
        print("Файл '%s' успешно обработан" % file_path)
    return result_parse


def parse_xml(file_path):
    """Парсит файл формата .xml по указанному пути.

             Входное значение file_path - путь к файлу

             Возвращает список из словарей в которых, значение - содержимое тега "<value>"
             в нутри тега <object> с атрибутом 'name', ключ - значение атрибута 'name',
    """
    with open(file_path) as xlm_file:
        doc = ElementTree.parse(xlm_file)
        objects = doc.iter("object")
        result_parse = []
        new_dict = {}
        for item in objects:
            key = item.attrib['name']
            if key in new_dict:
                result_parse.append(new_dict)
                new_dict = {}
            new_dict[key] = item.find("value").text
        else:
            result_parse.append(new_dict)
        print("Файл '%s' успешно обработан" % file_path)
    return result_parse
