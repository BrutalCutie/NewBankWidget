from .custom_errors import CardInfoError, DateFormatError
from .masks import mask_card_numbers


def get_masked_data(unmasked_data: str) -> str:
    """Функция принимает данные карты/счёта и возвращает их маски для сокрытия данных в виде строки"""

    # Делим имя и номер карты/счета на две переменных. Для маскировки номера используем \
    # уже созданную функцию mask_card_numbers из другого модуля
    operation_name = " ".join([x for x in unmasked_data.split() if x.isalpha()])
    nums = "".join([x for x in unmasked_data if x.isdigit()])

    if not operation_name or not nums:
        raise CardInfoError

    return f"{operation_name} {mask_card_numbers(nums)}"


def get_date(date_string: str) -> str:
    """Функция принимает дату в виде строки и возращает дату в необходимом формате"""

    # Отсекаем часы, оставляя только дату
    date = date_string.split("T", 1)[0]

    # Делим строку с датой на список, в котором будут: год, месяц, день
    formated_date_list = date.split("-")

    # Проверка на кол-во элементов списка. Вызов исключения если кол-во не равно 3 (ожидается [год, месяц, день])
    if len(formated_date_list) != 3:
        raise DateFormatError

    # Распаковываем полученный список в переменные
    year, month, day = formated_date_list

    return f"{day}.{month}.{year}"
