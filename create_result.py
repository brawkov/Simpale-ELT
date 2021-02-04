"""
    Модуль для формирования результата.
"""
from operator import itemgetter
import csv


def sum_unicode(string):
    """Выполняет суммирование ASCII кодов символов строки.
        Используется для функции sorted()

         Входное значение string - строка.

         Возвращает сумму ASCII кодов символов.
    """
    sum_ = 0
    for char in string:
        sum_ += ord(char)
    return sum_


def create_tsv(data, file_path):
    """Создает новый файл .tsv или перезаписывает существующий,
        если файл с таким именем существет.

        Входное значение data - данные для записи в файл в виде списка с списков значений для записи;
        file_path - путь + имя файла для сохранения файла.
    """
    if not file_path.endswith(".tsv"):
        file_path += ".tsv"

    with open(file_path, 'wt') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerows(data)
        print("Файл '%s' создан успешно" % file_path)


def sort_columns(data):
    """Упорядочивает колонки по возрастанию суммы ASCII кодов символов строки названия

        Входное значение data - данные для упорядочивания, в виде списка словарей, ключ - назване поля.
    """
    def _call_sum_unicode(string):
        return sum_unicode(string[0])

    sorted_data = []
    for item in data:
        sorted_data.append(dict(sorted(item.items(), key=_call_sum_unicode)))
    return sorted_data


def formatting_data(data, type_task):
    """Преобразует данные из списка словарей в список списков согласно заданию.

        Входное значение data - данные для упорядочивания, в виде списка словарей, ключ - назване поля;
        type_task - тип задания в виде строки, может принимать два значения: "advanced" и "basic"
    """
    if type_task == "advanced":
        data = sum_value(data)
    if type_task == "basic":
        data = sorted(data, key=itemgetter("D1"))
    formatted_data = []
    columns_name = []
    for row in data:
        columns_name.extend(row.keys())
    columns_name = sorted(set(columns_name), key=sum_unicode)
    formatted_data.append(columns_name)
    for row in data:
        new_row = []
        for key in columns_name:
            item = row.get(key)
            if item is None:
                item = " "
            new_row.append(item)
        formatted_data.append(new_row)
    return formatted_data


def sum_value(data):
    """Выполнет суммирование M1..Mn сгруппированные по уникальнным значениям комбинаций строк из D1...Dn,
       перед этим выполняя упорядочевание столбцов, сортировку по полю "D1".

       Входное значение data - данные для упорядочивания, в виде списка словарей, ключ - назване поля;
    """
    data = sort_columns(data)
    data = sorted(data, key=itemgetter("D1"))
    new_data = []
    for search_row in data.copy():
        keys = [item for item in dict.items(search_row) if item[0].startswith("D")]
        new_row = []
        delete_list = []
        for i in range(len(data)):
            if [item for item in dict.items(data[i]) if item[0].startswith("D")] == keys:
                new_row.append(data[i])
                delete_list.append(i)
        for i in range(len(delete_list)):
            data.pop(delete_list[i])
            if i + 1 < len(delete_list):
                delete_list[i + 1] -= 1
        if new_row:
            if len(new_row) > 1:
                keys = []
                for item in new_row:
                    keys.extend(item.keys())
                keys = sorted(set(keys), key=sum_unicode)
                sum_r = dict.fromkeys(keys, "0")
                for item in new_row:
                    for i in range(len(sum_r)):
                        if keys[i].startswith("M"):
                            if not item.get(keys[i]) is None:
                                sum_r[keys[i]] = int(sum_r[keys[i]]) + int(item.get(keys[i]))
                        else:
                            sum_r[keys[i]] = item.get(keys[i])
                new_data.append(sum_r)
            else:
                new_data.append(new_row[0])
    return new_data
