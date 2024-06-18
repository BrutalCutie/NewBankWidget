# Проект банковского виджета

## Описание

Данный проект является учебным и представляет собой практику над банковским виджетом

## Установка

1. Клонирование репозитория 
```
git clone https://github.com/BrutalCutie/NewBankWidget.git
```
2. Установите зависимостей проекта
```
poetry install
```

## Работа виджета
Запуск осуществляется в модуле main.py

## Классы:

### модуль utils:
- **Converter** - Вспомогательный класс для конвертации валюты.
    Создан с целью ускорить работу.
    Если обращение по API уже было выполнено и курс валюты к рублю известен:
        Код валюты и цена записываются в словарь {код валюты: цена}
    API конвертера "Exchange Rates Data API" https://apilayer.com/exchangerates_data-api
    ### методы - get_new_currency, get_currency

## Функции:

### модуль utils:
- **get_spaces_in_str** - Функция принимает строку. Опционально принимает аргемент sep_every(по умолчанию 4) = через сколько символов ставить символ второго опционального аргумента sep_symb(по умолчанию пробел)
- **get_transactions_list_from_file** - Функция принимает на вход путь до файла, в котором должен быть список
    словарей. Поддерживаемые расширения файлов: (**.csv / .json / .xclx**)
    Будет возвращен пустой список если:
        Файл не найден | Файл содержит НЕ список | Файл пустой
- **convert_to_json** - Функция для конвертации словарей по данным из DataFrame из файлов .csv | .excel.
    Возвращает список словарей с необходимым набором ключей и значений, предназначенных для работы.  

### модуль decorators:
- **log** - Функция-декоратор. Логгирует работу функции. Указание имени файла, создаёт в корне проекта файл логгирования. Без указания этого аргумента, будет делать вывод на консоль. 

### модуль widget:
- **get_masked_data** - Функция принимает данные карты/счёта и возвращает их маски для сокрытия данных в виде строки
- **get_by_date_operations** - Функция принимает дату в виде строки и возращает дату в необходимом формате

### модуль masks:
- **mask_card_numbers** - Функция принимает строку с цифрами на карте/счета и возвращает её скрытый вариант. Если: Карта - имеет 16 цифр, скрывает цифры с 7-12; Счёт - имеет 20 цифр(но это не точно), скрывает все цифры кроме последних 4

### модуль generators:
- **filter_by_currency** - Функция принимает на вход список словарей и возвращает итератор с операциями, если операция соответствует указанной currency
- **transaction_descriptions** - Функция принимает на вход список словарей с данными о транзакциях и возвращает итератор с описаниями транзакций по ключу "description"
- **card_number_generator** - Функция генерирует номера карт в формате XXXX XXXX XXXX XXXX, где X - цифра.
Начало берется с 0000 0000 0000 0000
    Пример вызова 1: start=1, end=4
        0000 0000 0000 0001,
        0000 0000 0000 0002,
        0000 0000 0000 0003,
        0000 0000 0000 0004

### модуль external_api:
- get_amount_in_rubles

## Исключения
- **CardInfoError** - Исключение, при неверном формате ввода карты/счета
- **DateFormatError** - Исключение при неверном формате подачи строки с датой

## Тесты
Производятся из пакета tests в котором находятся модули (test_ + имя тестируемго модуля из src)

### Запуск всех тестов:
```commandline
pytest
```

### Запуск всех тестов с информацией о покрытии:
```commandline
pytest --cov
```

## Конф.данные
Должны быть в файле .env. Пример данных для работы хранится в .env_sample
