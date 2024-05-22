from src.widget import get_date


def get_state(operations: list, state: str = "EXECUTED") -> list:
    """Функция возвращает список словарей в которых ключ state == параметру функции state(по умолчанию EXECUTED"""
    return [operation for operation in operations if operation["state"] == state]


def get_by_date_operations(operations: list, new_first: bool = True) -> list:
    """Функция возвращает упорядоченный список словарей по дате. По умолчанию(по убыванию)"""
    return sorted(operations, key=lambda op: get_date(op["date"]), reverse=new_first)
