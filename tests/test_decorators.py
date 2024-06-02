import os

from config import ROOT_DIR
from src.decorators import log


def test_log(capsys):

    @log()
    def square(x):
        """DocString test description"""
        return x * x

    print(square("as"))
    captured = capsys.readouterr()
    assert captured.out == (
        "======================ERROR=======================\n"
        "square error: <class 'TypeError'> Inputs: ('as',), {}\n"
        "can't multiply sequence by non-int of type 'str'\n"
        "================END ERROR MESSAGE=================\n\n"
    )
    print(square(3))
    captured = capsys.readouterr()
    assert captured.out == "square Inputs: (3,), {} - ok\n9\n"
    assert square.__doc__ == "DocString test description"


def test_log_with_file():

    file_name = "logger_test.log"
    logger_file_loc = os.path.join(ROOT_DIR, file_name)

    @log(file_name)
    def return_second_word(string: str) -> str:
        return f"{string} World"

    assert return_second_word("Hello") == "Hello World"
    # Проверяем создался ли файл. Удаляем файл, если был создан и тест прошел успешно
    assert os.path.exists(logger_file_loc) is True
    os.remove(logger_file_loc)


def test_log_error_with_file(capsys):

    file_name = "logger_test.log"
    logger_file_loc = os.path.join(ROOT_DIR, file_name)

    @log(file_name)
    def multi_string_numbers(string: int) -> str:
        return str(int(string) * 4)

    print(multi_string_numbers("error"))
    captured = capsys.readouterr()
    assert captured.out == "ERROR! Description in your log file\n"
    # Проверяем создался ли файл. Удаляем файл, если был создан и тест прошел успешно
    assert os.path.exists(logger_file_loc) is True
    os.remove(logger_file_loc)
