from typing import Any, Dict, List


def get_state(operations: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]] | None:
    """Функция возвращает список словарей в которых ключ state == параметру функции state(по умолчанию EXECUTED"""
    states_list: None | list = [operation for operation in operations if operation.get("state") == state]
    return states_list


def get_by_date_operations(operations: List[Dict[str, Any]], new_first: bool = True) -> List[Dict[str, Any]] | None:
    """Функция возвращает упорядоченный список словарей по дате. По умолчанию(по убыванию)"""
    sorted_by_date_list: None | list = sorted(operations, key=lambda op: op.get("date"), reverse=new_first)
    return sorted_by_date_list


def filter_by_descr(transactions: list[dict], search_field: str) -> list[dict]:
    """
    Функция принимает на вход список словарей с данными о транзакциях и возвращает только те,
    где есть совпадение по полю поиска(search_field) в ключе description
    :param transactions: список словарей с данными о транзакциях
    :param search_field: поле поиска в ключе description в списках транзакций
    :return: отфильтрованный список словарей с совпадениями
    """

    pass

