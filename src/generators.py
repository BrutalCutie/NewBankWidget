from typing import List, Dict, Any


def filter_by_currency(operations: List[Dict], currency: str) -> Dict:
    """
    Функция-генератор.

    :param operations: Принимает на вход список словарей
    :param currency: Ключ словаря в operations["operationAmount"]["currency"]["code"]
    :return: Возвращает итератор с ID операциями, если ID соответствует указанной currency

    """

    pass


def transaction_descriptions(operations: List) -> str:
    """
    Функция-генератор.

    :param operations: Принимает на вход список словарей с данными о транзакциях.
    :return: Итератор с описаниями транзакций по ключу "description"

    """

    pass


def card_number_generator(start: int, end: int) -> str:
    """
    Функция-генератор.
    Генерирует номера карт в формате XXXX XXXX XXXX XXXX, где X - цифра.
    Начало берется с 0000 0000 0000 0000
    Пример вызова 1: start=1, end=4
        0000 0000 0000 0001
        0000 0000 0000 0002
        0000 0000 0000 0003
        0000 0000 0000 0004

    Пример вызова 2: start=4, end=6
        0000 0000 0000 0004
        0000 0000 0000 0005
        0000 0000 0000 0006

    :return: Возвращает итератор с номерами карт

    """

    pass
