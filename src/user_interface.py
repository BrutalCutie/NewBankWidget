import os
import re

from config import DATA_DIR
from src.design import cprint
from src.processing import filter_by_currencies, filter_by_descr, get_by_date_operations, get_state
from src.utils import get_transactions_list_from_file
from src.widget import get_date, get_masked_data


class UserInterface:
    """
    Программа для взаимодействия с пользователем через интерфейс консоли.
    Запуск осуществляется вызовом класса
    """

    WORK_WITH_TEXT = (
        "Выберите необходимый пункт меню:\n\n"
        "1. Получить информацию о транзакциях из JSON-файла\n"
        "2. Получить информацию о транзакциях из CSV-файла\n"
        "3. Получить информацию о транзакциях из XLSX-файла\n\n"
    )
    WORK_WITH_PATTERN = r"из ([\w]+)"
    WORK_WITH_FILES = re.findall(WORK_WITH_PATTERN, WORK_WITH_TEXT)

    def __init__(self) -> None:
        """Запуск программы при вызове"""

        self.start()
        self.trans_data: list[dict] = [{"": ""}]  # заглушка для mypy

    def start(self) -> None:
        """Приветствие и ожидание ввода от пользователя, который будет означать расширение файла"""

        cprint(
            text="Программа: Привет!\n" "Добро пожаловать в программу работы с банковскими транзакциями.\n",
            text_color="blue",
            text_style="curve",
        )

        while True:

            cprint(self.WORK_WITH_TEXT, text_style="bold")
            mode_user_input = input("Пользователь: ")

            if mode_user_input in ["1", "2", "3"]:
                self.get_work_extension(mode_user_input)
                break

            cprint("\nОШИБКА: Введите пункт ТОЛЬКО из представленых.\n", text_color="red", text_style="bold")

    def get_work_extension(self, user_input: str) -> None:
        """Функция считывает данные из файла, согласно выбору пользователя"""

        user_input_index = int(user_input) - 1
        choosed_file_extention = self.WORK_WITH_FILES[user_input_index]
        file_name = f"operations.{choosed_file_extention.lower()}"
        choosed_file_path = os.path.join(DATA_DIR, file_name)
        self.trans_data = get_transactions_list_from_file(choosed_file_path)

        cprint(f"\nПрограмма: Выбрана работа с данными из {choosed_file_extention} файла\n", text_color="green")

        self.filter_by_state_question()

    def filter_by_state_question(self) -> None:
        """Фильтрация по статусу операции"""

        while True:
            cprint(
                text="Программа: Введите статус, по которому необходимо выполнить фильтрацию.\n"
                "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n\n",
                text_style="bold",
            )

            filter_user_input = input("Пользователь[EXECUTED]: ")

            if filter_user_input.upper() in ["EXECUTED", "CANCELED", "PENDING", ""]:

                if filter_user_input == "":
                    filter_user_input = "EXECUTED"

                break

            cprint(
                f'\nОШИБКА: Статус операции "{filter_user_input}" недоступен.\n', text_color="red", text_style="bold"
            )

        self.trans_data = get_state(self.trans_data, filter_user_input.upper())
        self.filter_by_date_question()

    def filter_by_date_question(self) -> None:
        """Сортировка по дате"""

        while True:
            cprint("\nПрограмма: Отсортировать операции по дате? да/нет\n", text_style="bold")
            by_date_user_answer = input("Пользователь[нет]: ")

            if by_date_user_answer.lower() == "да":

                self.get_course_question()
                break

            elif by_date_user_answer.lower() == "нет" or by_date_user_answer == "":
                self.get_in_rubbles()
                break

            cprint("\nОШИБКА: Ответ должен быть да/нет", text_color="red", text_style="bold")

    def get_course_question(self) -> None:
        """Если пользователь пожелал сортировать по дате. Ожидание ответа по возрастанию или по убыванию"""

        reverse = True
        while True:
            cprint("\nПользователь: по возрастанию/по убыванию\n", text_style="bold")
            course_user_answer = input("Пользователь[по убыванию]: ")

            if course_user_answer.lower() == "по возрастанию":
                reverse = False
                break

            elif course_user_answer.lower() == "по убыванию" or course_user_answer == "":
                break

            cprint("\nОШИБКА: Ответ должен быть по возрастанию/по убыванию", text_color="red", text_style="bold")

        self.trans_data = get_by_date_operations(self.trans_data, reverse)
        self.get_in_rubbles()

    def get_in_rubbles(self) -> None:
        """Фильтрация по валюте"""

        while True:
            cprint("\nПрограмма: Выводить только рублевые тразакции? да/Нет\n", text_style="bold")
            in_rubbles_user_answer = input("Пользователь[нет]: ")

            if in_rubbles_user_answer.lower() == "да":
                self.trans_data = filter_by_currencies(self.trans_data, ["RUB"])
                break

            elif in_rubbles_user_answer.lower() == "нет" or in_rubbles_user_answer == "":
                break

            cprint("\nОШИБКА: Ответ должен быть да/нет", text_color="red", text_style="bold")

        self.description_filter_question()

    def description_filter_question(self) -> None:
        """Фильтрация по ключевому слову в описании"""

        while True:
            cprint(
                "\nПрограмма: Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n",
                text_style="bold",
            )
            descr_f_user_answer = input("Пользователь[нет]: ")

            if descr_f_user_answer.lower() == "да":
                self.get_filter_word()
                break

            elif descr_f_user_answer.lower() == "нет" or descr_f_user_answer == "":
                self.show_results()
                break

            cprint("\nОШИБКА: Ответ должен быть да/нет", text_color="red", text_style="bold")

    def get_filter_word(self) -> None:
        """Ожидание слова фильтрации по ключевому слову"""

        cprint(
            "\nПрограмма: Введите строку, по которой будет фильтроваться список или оставьте поле пустым, "
            "чтобы не фильтровать\n",
            text_style="bold",
        )
        f_word_user_answer = input("Пользователь: ")
        self.trans_data = filter_by_descr(self.trans_data, f_word_user_answer)
        self.show_results()

    def show_results(self) -> None:
        """Распечатываем получившийся список операций в удобном формате"""

        trans_len = len(self.trans_data)
        cprint("\nПрограмма: Распечатываю итоговый список транзакций...\n", text_style="bold")

        if trans_len == 0:
            print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
            return None

        cprint(f"Программа: Всего банковских операций в выборке: {trans_len}\n", text_style="bold")

        for transaction in self.trans_data:
            date = get_date(transaction.get("date", "0000-00-00T00:00:00.00000"))
            descr = transaction.get("description", "Нет данных")
            from_: str = get_masked_data(transaction.get("from", "Нет данных"))
            to_: str = get_masked_data(transaction.get("to", "Нет данных"))
            summ = transaction.get("operationAmount", {}).get("amount", "Нет данных")
            currency_name = transaction.get("operationAmount", {}).get("currency", {}).get("name")

            print(
                f"""{date} {descr}
{from_ + " -> " + to_ if descr != "Открытие вклада" else to_}
Сумма: {summ} {currency_name}

"""
            )
