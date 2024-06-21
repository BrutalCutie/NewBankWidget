import json
import os
from unittest.mock import patch

import pytest

from config import ROOT_DIR
from src.utils import calculate_descriptions, get_spaces_in_str, get_transactions_list_from_file


def test_get_spaces_in_str():
    assert get_spaces_in_str("0000000000000000") == "0000 0000 0000 0000"
    assert get_spaces_in_str("1234567889010111") == "1234 5678 8901 0111"
    assert get_spaces_in_str("1234567889010111", 2) == "12 34 56 78 89 01 01 11"
    assert get_spaces_in_str("1234567889010111", sep_symb=",") == "1234,5678,8901,0111"


def test_get_spaces_in_str_type_err():
    with pytest.raises(TypeError):
        get_spaces_in_str(1234124)


def test_get_transactions_list_from_file(json_transactions_from_file):
    file_path = os.path.join(ROOT_DIR, "data", "operations.json")

    assert get_transactions_list_from_file(file_path) == json_transactions_from_file

    not_file_path = os.path.join(ROOT_DIR, "data", "special_error.json")
    assert get_transactions_list_from_file(not_file_path) == []


@patch("builtins.open", create=True)
def test_get_transactions_list_from_file_patch(mock_open):
    mock_file = mock_open.return_value.__enter__.return_value

    # Проверка на удачный результат. Что в файле список словарей
    mock_file.read.return_value = json.dumps([{"test": "test"}])
    assert get_transactions_list_from_file("test.json") == [{"test": "test"}]

    # Проверка на провал тип != список
    mock_file.read.return_value = json.dumps({})
    assert get_transactions_list_from_file("test.json") == []

    # Проверка на провал тип != список
    mock_file.read.return_value = json.dumps("testtest")
    assert get_transactions_list_from_file("test.json") == []

    # Проверка на провал "пустой файл"
    mock_file.read.return_value = ""
    assert get_transactions_list_from_file("test.json") == []


@patch("pandas.read_csv")
def test_get_transactions_list_from_file_csv(read_csv_mock, csv_excel_transactions_from_file):
    read_csv_mock.return_value.replace.return_value.to_dict.return_value = csv_excel_transactions_from_file
    assert get_transactions_list_from_file("test.csv") == [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "15.04.",
            "operationAmount": {"amount": "1234", "currency": {"name": "Euro", "code": "EUR"}},
            "description": "Test trans",
            "from": "Estonia",
            "to": "Russia",
        }
    ]


@patch("pandas.read_excel")
def test_get_transactions_list_from_file_excel(read_csv_mock, csv_excel_transactions_from_file):
    read_csv_mock.return_value.replace.return_value.to_dict.return_value = csv_excel_transactions_from_file
    assert get_transactions_list_from_file("test.xlsx") == [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "15.04.",
            "operationAmount": {"amount": "1234", "currency": {"name": "Euro", "code": "EUR"}},
            "description": "Test trans",
            "from": "Estonia",
            "to": "Russia",
        }
    ]


def test_calculate_descriptions(transactions):
    assert calculate_descriptions(transactions) == {
        "Перевод организации": 2,
        "Перевод с карты на карту": 1,
        "Перевод со счета на счет": 2,
    }
