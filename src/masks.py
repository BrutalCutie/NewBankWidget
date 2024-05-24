def mask_card_numbers(numbers: str) -> str:
    """
    Функция принимает строку с цифрами на карте/счета и возвращает её скрытый вариант.
    Если:
        Карта - имеет 16 цифр, скрывает цифры с 7-12;
        Счёт - имеет 20 цифр(но это не точно), скрывает все цифры кроме последних 4
    """

    number_length = len(numbers)

    # Если номер принадлежит карте
    if number_length == 16:

        hided_numbers = numbers[:6] + ("*" * 6) + numbers[-4:]
        # Разделяем скрытый номер по секциям в 4 цифры
        # fmt: off
        final_card_result = " ".join([hided_numbers[start:start + 4] for start in range(0, number_length, 4)])
        # fmt: on

        return final_card_result

    # Если номер принадлежит счёту
    return "**" + numbers[-4:]
