import re
import os

from config import DATA_DIR
from src.design import cprint
from src.processing import get_state, get_by_date_operations, filter_by_descr, filter_by_currencies
from src.utils import get_transactions_list_from_file


class UserInterface:

    WORK_WITH_TEXT = ("Выберите необходимый пункт меню:\n\n"
                      "1. Получить информацию о транзакциях из JSON-файла\n"
                      "2. Получить информацию о транзакциях из CSV-файла\n"
                      "3. Получить информацию о транзакциях из XLSX-файла\n\n")
    WORK_WITH_PATTERN = r'из ([\w]+)'
    WORK_WITH_FILES = re.findall(WORK_WITH_PATTERN, WORK_WITH_TEXT)

    def __init__(self):
        self.start()
        self.trans_data = None

    def start(self):

        cprint(text="Программа: Привет!\n"
                    "Добро пожаловать в программу работы с банковскими транзакциями.\n",
               text_color='blue',
               text_style='curve')

        while True:

            cprint(self.WORK_WITH_TEXT, text_style='bold')
            mode_user_input = input("Пользователь: ")

            if mode_user_input in ["1", "2", "3"]:
                self.get_work_extension(mode_user_input)

            cprint('\nОШИБКА: Введите пункт ТОЛЬКО из представленых.\n', text_color='red', text_style='bold')

    def get_work_extension(self, user_input: str) -> None:

        user_input_index = int(user_input) - 1
        choosed_file_extention = self.WORK_WITH_FILES[user_input_index]
        file_name = f'operations.{choosed_file_extention.lower()}'
        choosed_file_path = os.path.join(DATA_DIR, file_name)
        self.trans_data = get_transactions_list_from_file(choosed_file_path)

        cprint(f"\nПрограмма: Выбрана работа с данными из {choosed_file_extention} файла\n", text_color='green')

        self.filter_by_state()

    def filter_by_state(self):

        while True:
            cprint(text="Программа: Введите статус, по которому необходимо выполнить фильтрацию.\n"
                        "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n\n",
                   text_style='bold')

            filter_user_input = input("Пользователь: ")

            if filter_user_input.upper() in ['EXECUTED', 'CANCELED', 'PENDING']:
                break

            cprint(f"\nОШИБКА: Статус операции \"{filter_user_input}\" недоступен.\n", text_color='red', text_style='bold')

        self.trans_data = get_state(self.trans_data, filter_user_input.upper())
        self.filter_by_date()

    def filter_by_date(self):
        while True:
            cprint("\nПрограмма: Отсортировать операции по дате? да/нет\n", text_style='bold')
            by_date_user_answer = input("Пользователь[нет]: ")

            if by_date_user_answer.lower() == 'да':

                self.get_course()

            elif by_date_user_answer.lower() == 'нет' or by_date_user_answer == '':
                self.get_in_rubbles()

            cprint('\nОШИБКА: Ответ должен быть да/нет', text_color='red', text_style='bold')

    def get_course(self):

        reverse = True
        while True:
            cprint("\nПользователь: по возрастанию/по убыванию\n", text_style='bold')
            course_user_answer = input("Пользователь[по убыванию]: ")

            if course_user_answer.lower() == 'по возрастанию':
                reverse = False
                break

            elif course_user_answer.lower() == 'по убыванию' or course_user_answer == '':
                break

            cprint('\nОШИБКА: Ответ должен быть по возрастанию/по убыванию', text_color='red', text_style='bold')

        get_by_date_operations(self.trans_data, reverse)
        self.get_in_rubbles()

    def get_in_rubbles(self):

        while True:
            cprint("\nПрограмма: Выводить только рублевые тразакции? Да/Нет\n", text_style='bold')
            course_user_answer = input("Пользователь[нет]: ")

            if course_user_answer.lower() == 'да':
                pass

            elif course_user_answer.lower() == 'нет' or course_user_answer == '':
                pass


def main():
    """Главная функция для предоставления интерфейса для работы через консоль"""
    UserInterface()


if __name__ == "__main__":
    main()
