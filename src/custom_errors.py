class CardInfoError(Exception):
    """Исключение, при неверном формате ввода карты/счета"""

    def __str__(self) -> str:
        return "Enter correct operation info! Expected: <card | account> <numbers>"


class DateFormatError(Exception):
    """Исключение при неверном формате подачи строки с датой"""

    def __str__(self) -> str:
        return "Enter correct datestring. Example: 2018-07-11T02:26:18.671407"
