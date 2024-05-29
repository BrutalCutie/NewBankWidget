from src.utils import get_spaces_in_str


def test_get_spaces_in_str():
    assert get_spaces_in_str("0000000000000000") == "0000 0000 0000 0000"
    assert get_spaces_in_str("1234567889010111") == "1234 5678 8901 0111"
    assert get_spaces_in_str("1234567889010111", 2) == "12 34 56 78 89 01 01 11"
    assert get_spaces_in_str("1234567889010111", sep_symb=",") == "1234,5678,8901,0111"
