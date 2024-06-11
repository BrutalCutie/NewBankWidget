import requests
import dotenv
import os


class Converter:
    """
    Вспомогательный класс для конвертации валюты.
    Создан с целью ускорить работу.
    Если обращение по API уже было выполнено и курс валюты к рублю известен:
        Код валюты и цена записываются в словарь {код валюты: цена}
    API конвертера "Fixer API" https://apilayer.com/marketplace/fixer-api
    """

    # Загрузка конф. данных из dotenv
    dotenv.load_dotenv()
    known_currencies = {}
    CURRENCY_URL = "https://api.apilayer.com/fixer/convert?to={_to}&from={_from}&amount={amount}"
    HEADER = {'apikey': os.getenv('CONVERTER_API')}
    _to = "RUB"

    @staticmethod
    def get_currency(code: str) -> float:

        if code in Converter.known_currencies:
            return Converter.known_currencies[code]

        return Converter.get_new_currency(code)

    @staticmethod
    def get_new_currency(code: str) -> float:
        response = requests.get(url=Converter.CURRENCY_URL.format(_to=Converter._to, _from=code, amount=1),
                                headers=Converter.HEADER)

        result = response.json()['result']

        Converter.known_currencies[code] = result

        return result


def get_amount_in_rubles(trans_data: dict) -> float | None:
    """

    :param trans_data:
    :return:
    """

    if not trans_data.get("operationAmount"):
        return None

    amount = float(trans_data['operationAmount']['amount'])
    currency = trans_data['operationAmount']['currency']['code']

    if currency != "RUB":
        currency_per_unit_price = Converter.get_currency(currency)
        converted_amount = amount * currency_per_unit_price
        return converted_amount
    print(f"{amount} {currency}")
    return amount


if __name__ == '__main__':
    from src.utils import get_transactions_list_from_file
    from config import ROOT_DIR
    import os

    file_path = os.path.join(ROOT_DIR, 'data', 'operations.json')

    trans = get_transactions_list_from_file(file_path)

    for i in trans:
        if i:
            get_amount_in_rubles(i)

