import json
import sys
import time


def get_spaces_in_str(string: str, sep_every: int = 4, sep_symb: str = " ") -> str:
    """
    Функция принимает строку, вставляет sep_symb через каждые sep_every и возвращает новую строку

    :param string: Строка которая берется за исходную для изменений
    :param sep_every: Через сколько символов будет вставляться sep_symb
    :param sep_symb: Какой символ будет вставляться через каждые sep_every символов
    :return: Измененная строка с новым(-и) символом(-ами), согласно sep_every и sep_symb
    """

    new_string = ""
    node = 0
    for symb in string:

        if node % sep_every == 0 and node != 0:
            new_string += sep_symb

        new_string += symb
        node += 1

    return new_string


def get_transactions_list_from_file(file_path: str) -> list:
    """
    Функция принимает на вход путь до файла, в котором должен быть список
    словарей.
    Будет возвращен пустой список если:
        Файл не найден | Файл содержит НЕ список | Файл пустой

    пауза(time.sleep) вызывается для предотвращения "перепрыгивания" сообщений

    :param file_path: путь до файла + название файла
    :return: считанный с файла список словарей
    """

    # Оборачиваем код для отлавливания ошибки, когда файла не существует.
    # В случае отсутствия - вернуть сообщение и пустой список

    try:
        with open(file_path, 'r', encoding='utf8') as file:

            # Так как with open(... нельзя считать дважды, читаем и сохраняем результат чтения в переменную
            static_file = file.read()

            # Проверка что файл не пустой
            if not len(static_file) > 0:
                sys.stderr.write(f"NOTE: Expected list[dict] in file, got: nothing\n")
                time.sleep(0.05)
                return []

            result = json.loads(static_file)

            # Возвращаем пустой список если в файле НЕ список
            if not isinstance(result, list):
                file_type = type(result)
                sys.stderr.write(f"NOTE: Expected contain: {type([])} in file, got: {file_type}\n")
                time.sleep(0.05)
                return []

        return result

    except FileNotFoundError:
        sys.stderr.write(f"NOTE: File not founded, returned empty list\n")
        time.sleep(0.05)
        return []
