import pytest

from src.generators import card_number_generator, transaction_descriptions, filter_by_currency


def test_filter_by_currency(transactions):
    generator = filter_by_currency(transactions, 'USD')
    assert next(generator) == 939719570
    assert next(generator) == 142264268
    assert next(generator) == 895315941


def test_filter_skip_keyerror(transactions):
    generator = filter_by_currency([{
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        }], 'USD')
    with pytest.raises(ValueError):
        next(generator)


def test_filter_by_currency_empty_list_exception(transactions):
    with pytest.raises(ValueError):
        next(filter_by_currency(transactions, 'U'))


@pytest.mark.parametrize("wrong_type", [
    ('nothing',),
    ({'nothing': True}),
    (123,)
])
def test_filter_by_currency_wrong_type_exception_many(wrong_type):
    with pytest.raises(TypeError):
        next(filter_by_currency(wrong_type, 'USD'))


def test_card_number_generator():
    pass


def test_transaction_descriptions():
    pass
