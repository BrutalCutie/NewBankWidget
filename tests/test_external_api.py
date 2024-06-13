from unittest.mock import patch

from src.external_api import Converter, get_amount_in_rubles


@patch("requests.get")
def test_get_amount_in_rubles(get_mock):
    json_transactions_from_file = [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589",
        },
        {
            "id": 41428829,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
            "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "MasterCard 7158300734726758",
            "to": "Счет 35383033474447895560",
        },
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
    ]
    mock = get_mock.return_value
    mock.json.return_value = {"result": 89.321}

    for trans in json_transactions_from_file:
        assert isinstance(get_amount_in_rubles(trans), float | None)


@patch("requests.get")
def test_converter_get_currency(get_currency_mock):
    mock = get_currency_mock.return_value
    mock.json.return_value = {"result": 89.321}

    assert Converter.get_currency("EUR") == 89.321
    assert Converter.get_currency("USD") == 89.321


@patch("requests.get")
def test_converter_get_new_currency(get_currency_mock):
    mock_work = get_currency_mock.return_value

    mock_work.json.return_value = {"result": 89.321}
    assert Converter.get_new_currency("USD") == 89.321
