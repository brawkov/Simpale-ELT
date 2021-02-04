import argparse

import parsers_file
import create_result


def run_parsers(param):
    result = []
    for file_path in param:
        if file_path.endswith(".csv"):
            result.extend(parsers_file.parse_csv(file_path))
        else:
            if file_path.endswith(".json"):
                result.extend(parsers_file.parse_json(file_path))
            else:
                if file_path.endswith(".xml"):
                    result.extend(parsers_file.parse_xml(file_path))
                else:
                    print("Файл", file_path, "не соответствует ни одному из поддерживаемых типов файлов.")
    return result


def main():
    parser = argparse.ArgumentParser(prog='simple_elt', description='Simple ELT')
    parser.add_argument('file_path', action='store', help='Путь к файлу', nargs='+')
    args = parser.parse_args()
    if len(args.file_path) >= 1:
        exist_all_file = True
        for file_path in args.file_path:
            if not (parsers_file.exist_file(file_path)):
                exist_all_file = False
        if exist_all_file:
            result = run_parsers(args.file_path)
            formatted_data_basic = create_result.formatting_data(result, "basic")
            formatted_data_advanced = create_result.formatting_data(result, "advanced")
            create_result.create_tsv(formatted_data_basic, "result/basic.result")
            create_result.create_tsv(formatted_data_advanced, "result/advanced.result")
    else:
        print("Укажите пожалуйста файлы.")


if __name__ == '__main__':
    main()
