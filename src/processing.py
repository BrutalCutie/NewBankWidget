import re
from typing import Any, Dict, List


def get_state(operations: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Функция возвращает список словарей в которых ключ state == параметру функции state(по умолчанию EXECUTED"""
    states_list: list[dict] = [operation for operation in operations if operation.get("state", "") == state]
    return states_list


def get_by_date_operations(operations: List[Dict[str, Any]], new_first: bool = True) -> List[Dict[str, Any]]:
    """Функция возвращает упорядоченный список словарей по дате. По умолчанию(по убыванию)"""
    sorted_by_date_list = sorted(operations, key=lambda op: op["date"], reverse=new_first)
    return sorted_by_date_list


def filter_by_descr(transactions: list[dict], search_field: str) -> list[dict]:
    """
    Функция принимает на вход список словарей с данными о транзакциях и возвращает только те,
    где есть совпадение по полю поиска(search_field) в ключе description
    :param transactions: Список словарей с данными о транзакциях
    :param search_field: Поле поиска в ключе description в списках транзакций
    :return: Отфильтрованный список словарей с совпадениями
    """
    tmp = []
    pattern = rf"{search_field}\w*"

    for transaction in transactions:
        result = re.findall(pattern, transaction["description"], flags=re.IGNORECASE)

        if result:
            tmp.append(transaction)

    return tmp


def filter_by_currencies(transactions: list[dict], currencies: list[str]) -> list[dict]:
    """
    Функция принимает на вход список словарей с данными о транзакциях и возвращает только те,
    где есть совпадение code в currencies.
    :param transactions: Список словарей с данными о транзакциях
    :param currencies: Список или строка с валютой, которые останутся в списке
    :return: Отфильтрованный список словарей с совпадениями по валюте
    """

    return [x for x in transactions if x.get("operationAmount", {}).get("currency", {}).get("code") in currencies]
