from src.processing import get_by_date_operations, get_state
from src.widget import get_date, get_masked_data

# проверка функции get_masked_data
print(get_masked_data("Счет 64686473678894779589"))

# проверка функции get_date
print(get_date("2018-07-11T02:26:18.671407"))

# проверка функций get_state и get_by_date_operations
example = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]

print(get_state(example))
print(get_state(example, state="CANCELED"))

print(get_by_date_operations(example))
print(get_by_date_operations(example, new_first=False))
