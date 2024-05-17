class WrongCardInfoError(Exception):
    """ Исключение, при неверном формате ввода карты/счета """
    def __str__(self):
        return 'Enter correct operation info! Expected: <card | account> <numbers>'
