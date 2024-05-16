from .masks import mask_card_numbers


class WrongCardInfoError(Exception):
    pass


def get_operation_name(operation_info: str) -> str:
    """ Функция принимает данные карты/счёта и возвращает только имя операции(счёт/Visa/Master и тд """

    # Перебираем посимвольно строку. Если следующий символ цифра - возвращаем имя операции
    last_index = len(operation_info) - 1
    node_index = 0
    for index, symb in enumerate(operation_info):
        node_index = index + 1
        if index == last_index or symb.isdigit():
            # поднимаем ошибку, в случае если обрабатываем последний символ строки, но так и не получили имя операции
            raise WrongCardInfoError('Enter correct operation info! Expected: <op.name> <numbers>')

        elif operation_info[index+1].isdigit():
            break
            # возвращаем имя операции
    return operation_info[:node_index]


def get_masked_data(unmasked_data: str) -> str:
    """ Функция принимает данные карты/счёта и возвращает их маски для сокрытия данных в виде строки """

    # Делим имя и номер карты/счета на две переменных. Для маскировки номера используем \
    # уже созданную функцию mask_card_numbers из другого модуля
    operation_name = get_operation_name(unmasked_data)
    numbers = ''.join([x for x in unmasked_data if x.isdigit()])

    return operation_name + mask_card_numbers(numbers)


def get_date(date_string: str) -> str:
    """ Функция принимает дату в виде строки и возращает дату в необходимом формате """
    pass



