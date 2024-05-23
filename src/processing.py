from typing import Any, Dict, List


def get_state(operations: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]] | None:
    """Функция возвращает список словарей в которых ключ state == параметру функции state(по умолчанию EXECUTED"""
    states_list: None | list = [operation for operation in operations if operation.get("state") == state]
    return states_list


def get_by_date_operations(operations: List[Dict[str, Any]], new_first: bool = True) -> List[Dict[str, Any]] | None:
    """Функция возвращает упорядоченный список словарей по дате. По умолчанию(по убыванию)"""
    sorted_by_date_list: None | list = sorted(operations, key=lambda op: op.get("date"), reverse=new_first)
    return sorted_by_date_list
