from .masks import mask_card_numbers
from .custom_errors import WrongCardInfoError


def get_masked_data(unmasked_data: str) -> str:
    """ Функция принимает данные карты/счёта и возвращает их маски для сокрытия данных в виде строки """

    # Делим имя и номер карты/счета на две переменных. Для маскировки номера используем \
    # уже созданную функцию mask_card_numbers из другого модуля
    operation_name = ' '.join([x for x in unmasked_data.split() if x.isalpha()])
    nums = ''.join([x for x in unmasked_data if x.isdigit()])

    if not operation_name or not nums:
        raise WrongCardInfoError()

    return f"{operation_name} {mask_card_numbers(nums)}"


def get_date(date_string: str) -> str:
    """ Функция принимает дату в виде строки и возращает дату в необходимом формате """
    pass
