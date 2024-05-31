import logging
from typing import Callable, Any, Union


def log(filepath: str | None = None, exc_info: bool = False) -> Union[Callable, None]:
    """
        Функция-декоратор.
        Не изменяет поведение оборачиваемой функции.
        Производит логгирование выполнения работы функции.
        Если аргумент filepath остаётся пустым(по умолчанию None) - вывод прооиходит на консоль.
        В ином случае создаёт файл, с логами об успешном выполнении или об ошибке которая произошла при выполнении.

        :param filepath: по умолчанию None. Название файла для логгирования.
        :param exc_info: по умолчанию False. Вывод подробной информации об ошибке.
        :return: Фунцию или None в случае ошибки
        """

    def wrapper(func: Callable) -> Union[Callable, None]:
        def inner(*args: tuple, **kwargs: dict) -> Any:
            logging.basicConfig(filename=filepath, level=10)

            try:
                result = func(*args, **kwargs)
                logging.debug(f"{func.__name__} Inputs: {args}, {kwargs} - ok")
                return result
            except Exception as err:
                logging.error(f"{func.__name__} error: {err.__class__} Inputs: {args}, {kwargs}\n{str(err)}",
                              exc_info=exc_info)
                return None

        return inner

    return wrapper


if __name__ == '__main__':

    @log(exc_info=False)
    def square(x: int, y=2):
        return x * x * y
