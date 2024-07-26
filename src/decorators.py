import os
from functools import wraps
from typing import Any, Callable, Union

from config import ROOT_DIR


def log(filepath: str | None = None) -> Union[Callable, None]:
    """
    Функция-декоратор.
    Не изменяет поведение оборачиваемой функции.
    Производит логгирование выполнения работы функции.
    Если аргумент filepath остаётся пустым(по умолчанию None) - вывод прооиходит на консоль.
    В ином случае создаёт файл, с логами об успешном выполнении или об ошибке которая произошла при выполнении.

    :param filepath: по умолчанию None. Название файла для логгирования.
    :return: Фунцию или None в случае ошибки
    """

    def wrapper(func: Callable) -> Union[Callable, None]:
        @wraps(func)
        def inner(*args: tuple, **kwargs: dict) -> Any:

            try:
                success_text_data = f"{func.__name__} Inputs: {args}, {kwargs} - ok"
                result = func(*args, **kwargs)

                if not filepath:
                    print(success_text_data)
                else:
                    log_file_path = os.path.join(ROOT_DIR, filepath)
                    with open(log_file_path, "a", encoding="utf8") as logger_file:
                        logger_file.write(success_text_data + "\n")

                return result

            except Exception as err:
                error_text_data = f"{func.__name__} error: {err.__class__} Inputs: {args}, {kwargs}\n{str(err)}"
                if not filepath:
                    print(f"{'ERROR':=^50}")
                    print(error_text_data)
                    print(f"{'END ERROR MESSAGE':=^50}")
                    return ""
                else:
                    log_file_path = os.path.join(ROOT_DIR, filepath)
                    with open(log_file_path, "a", encoding="utf8") as logger_file:
                        logger_file.write(error_text_data + "\n")

                    return "ERROR! Description in your log file"

        return inner

    return wrapper
