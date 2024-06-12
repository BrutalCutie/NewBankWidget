from unittest.mock import Mock, patch

import requests

from src.external_api import Converter, get_amount_in_rubles


def test_get_amount_in_rubles(json_transactions_from_file):
    mock_currency = Mock(return_value={"result": 89.321})
    requests.get.json = mock_currency
    for trans in json_transactions_from_file:
        assert isinstance(get_amount_in_rubles(trans), float | None)


@patch("src.external_api.Converter.get_new_currency")
def test_converter_get_currency(get_currency_mock):
    get_currency_mock.return_value = 89.321

    Converter.known_currencies["EUR"] = 100.0
    assert Converter.get_currency("EUR") == 100.0
    assert Converter.get_currency("USD") == 89.321


@patch("requests.get")
def test_converter_get_new_currency(get_currency_mock):
    mock_work = get_currency_mock.return_value

    mock_work.json.return_value = {"result": 89.321}
    assert Converter.get_new_currency("USD") == 89.321
