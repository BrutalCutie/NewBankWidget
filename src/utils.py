import json
import logging
import os
import re
from collections import defaultdict

import numpy as np
import pandas as pd

from config import LOGS_DIR

logger = logging.getLogger("utils")

logger_file_handler = logging.FileHandler(os.path.join(LOGS_DIR, "utils.log"), encoding="utf8", mode="w")
logger_formatter = logging.Formatter("%(asctime)s - %(levelname)s - FUNC(%(funcName)s): %(message)s")
logger_file_handler.setFormatter(logger_formatter)
logger.addHandler(logger_file_handler)
logger.setLevel(logging.DEBUG)


def get_spaces_in_str(string: str, sep_every: int = 4, sep_symb: str = " ") -> str:
    """
    Функция принимает строку, вставляет sep_symb через каждые sep_every и возвращает новую строку

    :param string: Строка, которая берется за исходную для изменений
    :param sep_every: Через сколько символов будет вставляться sep_symb
    :param sep_symb: Какой символ будет вставляться через каждые sep_every символов
    :return: Измененная строка с новым(-и) символом(-ами), согласно sep_every и sep_symb
    """

    if not isinstance(string, str):
        logger.error(f"Ошибка arg(string) must be str class, given {type(string)}. arg(string) = {string}")
        raise TypeError(f"arg(string) must be str class, given {type(string)}")

    re_pattern = r"[\d*]{" + str(sep_every) + r"}"
    new_string_list = re.findall(re_pattern, string)

    return f"{sep_symb}".join(new_string_list)


def get_transactions_list_from_file(file_path: str) -> list:
    """
    Функция принимает на вход путь до файла, в котором должен быть список
    словарей. Поддерживаемые расширения файлов: [.csv, .json, .xclx]
    Будет возвращен пустой список если:
        Файл не найден | Файл содержит НЕ список | Файл пустой


    :param file_path: путь до файла + название файла
    :return: считанный с файла список словарей
    """

    # записываем расширение файла
    file_extension = os.path.splitext(file_path)[-1]

    # Оборачиваем код для отлавливания ошибки, когда файла не существует.
    # В случае отсутствия файла - пустой список
    # В случае пустого файла - пустой список

    try:
        if file_extension == ".csv":
            file_data = pd.read_csv(file_path, delimiter=";", encoding="utf8")
            # Меняем nan -> None
            file_data = file_data.replace({np.nan: None})

            # Конвертируем DataFrame в необходимого формата list[dict]
            file_dict_data = file_data.to_dict("records")

            result = convert_to_json(file_dict_data)

        elif file_extension == ".xlsx":
            file_data = pd.read_excel(file_path)

            # Меняем nan -> None
            file_data = file_data.replace({np.nan: None})

            # Конвертируем DataFrame в необходимого формата list[dict]
            file_dict_data = file_data.to_dict("records")
            result = convert_to_json(file_dict_data)

        else:
            with open(file_path, encoding="utf8") as file:
                result = json.load(file)

        # Возвращаем пустой список если в файле НЕ список
        if not isinstance(result, list):
            logger.error("Возвращаем пустой список. В файле НЕ список")
            return []

        logger.info(f"Содержимое файла успешно передано. Расширение файла {file_extension}")
        return result

    # Возвращаем пустой список если файл не найден
    except FileNotFoundError:
        logger.error("Возвращаем пустой список. Файл не найден")
        return []

    # Возвращаем пустой список если файл пустой
    except json.decoder.JSONDecodeError:
        logger.error("Возвращаем пустой список. Файл пустой")
        return []


def convert_to_json(trans_data: list[dict]) -> list[dict]:
    """
    Функция для конвертации словарей по данным из DataFrame из файлов .csv | .excel.
    Возвращает список словарей с необходимым набором ключей и значений, предназначенных для работы.

    :param trans_data: Неотфильтрованные данные списка словарей
    :return: Список словарей с необходимым набором ключей и значений, предназначенных для работы
    """

    tmp = []

    for transaction in trans_data:
        tmp.append(
            {
                "id": transaction.get("id"),
                "state": transaction.get("state"),
                "date": transaction.get("date"),
                "operationAmount": {
                    "amount": transaction.get("amount"),
                    "currency": {"name": transaction.get("currency_name"), "code": transaction.get("currency_code")},
                },
                "description": transaction.get("description"),
                "from": transaction.get("from"),
                "to": transaction.get("to"),
            }
        )

    return tmp


def calculate_descriptions(trans_data: list[dict]) -> dict[str, int]:
    """
    Функция принимает список словарей с данными о транзакциях и возвращает словарь,
    в котором ключи — это названия категорий, а значения — это количество операций в каждой категории.
    :param trans_data: Список словарей с данными о транзакциях
    :return: Словарь с категориями и количество их упоминания
    """

    tmp: dict = defaultdict(int)

    for transaction in trans_data:
        descr = transaction.get("description")

        if descr:
            tmp[descr] += 1

    return tmp
