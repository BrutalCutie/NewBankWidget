from typing import Any, Dict, Iterator, List

from src.utils import get_spaces_in_str


def filter_by_currency(operations: List[Dict[Any, Any]], currency: str) -> Iterator:
    """
    Функция-генератор.

    :param operations: Принимает на вход список словарей
    :param currency: Ключ словаря в operation["operationAmount"]["currency"]["code"]
    :return: Возвращает итератор с операциями, если операция соответствует указанной currency

    """

    # Проверяем тип. Если это не список - выбрасываем ошибку
    if not isinstance(operations, list):
        raise TypeError(f"Expected {list} but {type(operations)} was given")

    # Создаём временный контейнер. Предназначение: сначала мы проходим циклом по нашему списку словарей
    # чтобы сократить ожидание после каждого вывода. Пример: имеем список длиной в 1 милл. операций.
    # Из всего списка подходит id только первого и последнего элемента. Ожидание между первой и второй пройдет время.
    # С контейнером мы сначала ждем прохода цикла и получаем результат.
    iterator_list = []

    for operation in operations:

        # Отлавливаем ошибку, пропускаем итерацию и продолжаем цикл, если в словаре нету необходимого ключа
        try:
            transaction_currency = operation["operationAmount"]["currency"]["code"]
        except KeyError:
            continue

        # Если в объекте полное совпадение по искомой валюте - добавляем во временный контейнер
        if transaction_currency == currency.upper():
            iterator_list.append(operation)

    for transaction_data in iterator_list:
        yield transaction_data


def transaction_descriptions(operations: List[Dict[Any, Any]]) -> Iterator:
    """
    Функция-генератор.

    :param operations: Принимает на вход список словарей с данными о транзакциях.
    :return: Итератор с описаниями транзакций по ключу "description"

    """
    # Проверяем тип. Если это не список - выбрасываем ошибку
    if not isinstance(operations, list):
        raise TypeError(f"Expected {list} but {type(operations)} was given")

    for operation in operations:
        if operation.get("description"):
            yield operation["description"]


def card_number_generator(start: int, end: int) -> Iterator:
    """
    Функция-генератор.
    Генерирует номера карт в формате XXXX XXXX XXXX XXXX, где X - цифра.
    Начало берется с 0000 0000 0000 0000
    Пример вызова 1: start=1, end=4
        0000 0000 0000 0001,
        0000 0000 0000 0002,
        0000 0000 0000 0003,
        0000 0000 0000 0004

    Пример вызова 2: start=4, end=6
        0000 0000 0000 0004,
        0000 0000 0000 0005,
        0000 0000 0000 0006

    :return: Возвращает итератор с номерами карт

    """

    static_num = "0000000000000000"
    for last_num in range(start, end + 1):
        last_num_len = len(str(last_num))
        new_num = static_num[:-last_num_len] + str(last_num)
        yield get_spaces_in_str(new_num)
