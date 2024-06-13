import pytest

from src.masks import mask_card_numbers


@pytest.mark.parametrize(
    "nums, expected",
    (
        ("1596837868705199", "1596 83** **** 5199"),
        ("64686473678894779589", "**9589"),
        ("7158300734726758", "7158 30** **** 6758"),
        ("35383033474447895560", "**5560"),
        ("6831982476737658", "6831 98** **** 7658"),
        ("8990922113665229", "8990 92** **** 5229"),
        ("899092211366522912312311523523523", "**3523"),
    ),
)
def test_mask_card_numbers(nums, expected):
    assert mask_card_numbers(nums) == expected


def test_mask_card_numbers_type_err():
    with pytest.raises(TypeError):
        mask_card_numbers(1412412412312313)
