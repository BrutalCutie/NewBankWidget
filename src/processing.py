def get_state(operations: list, state: str = 'EXECUTED') -> list:
    """Функция возвращает список словарей в которых ключ state == параметру функции state(по умолчанию EXECUTED"""
    return [operation for operation in operations if operation['state'] == state]


def get_by_date_operations(operations: list, new_first: bool = True) -> list:
    """Функция возвращает упорядоченный список словарей по дате"""
    pass



