import pytest

from src.custom_errors import CardInfoError, DateFormatError
from src.widget import get_date, get_masked_data


@pytest.mark.parametrize(
    "str_date, expected",
    [
        ("2019-07-03T18:35:29.512364", "03.07.2019"),
        ("2018-10-14T08:21:33.419441", "14.10.2018"),
        ("2018-09-12T21:27:25.241689", "12.09.2018"),
        ("2018-06-30T02:08:58.425572", "30.06.2018"),
        (None, "Нет данных")
    ],
)
def test_get_date(str_date, expected):
    assert get_date(str_date) == expected


def test_get_date_wrong_format():
    with pytest.raises(DateFormatError):
        get_date("2018-30T02:08:58")


@pytest.mark.parametrize(
    "unmasked_data, expected",
    [
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
        ("Visa Platinum 8990 9221 1366 5229", "Visa Platinum 8990 92** **** 5229"),
    ],
)
def test_get_masked_data(unmasked_data, expected):
    assert get_masked_data(unmasked_data) == expected


def test_get_masked_data_wrong_format_1():
    with pytest.raises(CardInfoError):
        get_masked_data("I am a card, trust me")


def test_get_masked_data_wrong_format_2():
    with pytest.raises(CardInfoError):
        get_masked_data("1414 4534 5346 8434")
