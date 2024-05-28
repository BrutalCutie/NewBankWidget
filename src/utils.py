def get_spaces_in_str(string: str, sep_every: int = 4, sep_symb: str = " "):
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





if __name__ == '__main__':
    print(get_spaces_in_str("0000000000000000"))

