import os

import dotenv
import requests


class Converter:
    """
    Вспомогательный класс для конвертации валюты.
    Создан с целью ускорить работу.
    Если обращение по API уже было выполнено и курс валюты к рублю известен:
        Код валюты и цена записываются в словарь {код валюты: цена}
    API конвертера "Exchange Rates Data API" https://apilayer.com/marketplace/exchangerates_data-api
    """

    # Загрузка конфиденциальных данных из dotenv
    dotenv.load_dotenv()
    # Контейнер для валют и их цен
    known_currencies: dict[str, float] = {}
    CURRENCY_URL = "https://api.apilayer.com/exchangerates_data/convert?to={_to}&from={_from}&amount={amount}"
    HEADER = {"apikey": os.getenv("CONVERTER_API")}
    _to = "RUB"

    @staticmethod
    def get_currency(code: str) -> float | str:
        """
        Функция принимает на вход код валюты (напр. EUR;USD), проверяет была ли
        уже получена информация по данной валюте и возвращает курс по отношению к рублю.

        :param code: Код валюты
        :return: Курс по отношению к рублю
        """

        # Отсекаем транзакции без кода валюты
        if not code:
            return "Код валюты отсутствует"

        # Проверяем, есть ли информация по валюте в классе
        elif code in Converter.known_currencies:
            return Converter.known_currencies[code]

        # Если информации о такой валюте ещё не было - обращаемся к get_new_currency
        return Converter.get_new_currency(code)

    @staticmethod
    def get_new_currency(code: str) -> float:
        """
        Функция принимает на вход код валюты (напр. EUR;USD), записывает данные во внутренний словарь
        и возвращает курс code валюты по отношению к рублю

        :param code: код валюты
        :return:  курс по отношению к рублю
        """
        response = requests.get(
            url=Converter.CURRENCY_URL.format(_to=Converter._to, _from=code, amount=1), headers=Converter.HEADER
        )

        result: float = response.json()['result']

        Converter.known_currencies[code] = result

        return result


def get_amount_in_rubles(trans_data: dict) -> float | None:
    """
    Функция получает на вход словарь с информацией о транзакции.
    Возвращает информацию об сумме транзакции. Если валюта происведена
    в отличной от рубля валюте - конвертируется через вспомагательный класс Converter


    :param trans_data: словарь с информацией о транзакции
    :return: сумма транзакции в рублях
    """

    # если информация об сумме транзакции отсутствует, возворащаем None
    if not trans_data.get("operationAmount"):
        return None

    amount = float(trans_data["operationAmount"]["amount"])
    currency = trans_data["operationAmount"]["currency"]["code"]

    # если валюта транзакции не в рублях, получаем данные от Converter
    if currency != "RUB":
        currency_per_unit_price = Converter.get_currency(currency)
        converted_amount = amount * currency_per_unit_price
        return converted_amount
    return amount
