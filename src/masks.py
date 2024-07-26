import logging
import os

from config import LOGS_DIR
from src.utils import get_spaces_in_str

logger = logging.getLogger("masks")

logger_file_handler = logging.FileHandler(os.path.join(LOGS_DIR, "masks.log"), encoding="utf8", mode="w")
logger_formatter = logging.Formatter("%(asctime)s - %(levelname)s - FUNC(%(funcName)s): %(message)s")
logger_file_handler.setFormatter(logger_formatter)
logger.addHandler(logger_file_handler)
logger.setLevel(logging.DEBUG)


def mask_card_numbers(numbers: str) -> str:
    """
    Функция принимает строку с цифрами на карте/счета и возвращает её скрытый вариант.
    Если:
        Карта - имеет 16 цифр, скрывает цифры с 7-12;
        Счёт - имеет 20 цифр(но это не точно), скрывает все цифры кроме последних 4
    """

    if not isinstance(numbers, str):
        logger.error(f"Ошибка arg(string) must be str class, given {type(numbers)}. arg(string) = {numbers}")
        raise TypeError(f"arg(string) must be str class, given {type(numbers)}")

    number_length = len(numbers)

    # Если номер принадлежит карте
    if number_length == 16:

        hided_numbers = numbers[:6] + ("*" * 6) + numbers[-4:]
        # Разделяем скрытый номер по секциям в 4 цифры
        final_card_result = get_spaces_in_str(hided_numbers)

        logger.info(f"Передана карта {numbers}")

        return final_card_result

    # Если номер принадлежит счёту
    logger.info(f"Передан счёт {numbers}")

    return "**" + numbers[-4:]
