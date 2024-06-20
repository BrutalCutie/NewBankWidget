import re
import os

from config import DATA_DIR
from src.design import cprint
from src.processing import get_state
from src.utils import get_transactions_list_from_file


class UserInterface:
    is_greetings_sended = False

    USER = "Пользователь: "

    GREETINGS_TEXT = ("Программа: Привет!\n"
                      "Добро пожаловать в программу работы с банковскими транзакциями.\n")

    WORK_WITH_TEXT = ("Выберите необходимый пункт меню:\n\n"
                      "1. Получить информацию о транзакциях из JSON-файла\n"
                      "2. Получить информацию о транзакциях из CSV-файла\n"
                      "3. Получить информацию о транзакциях из XLSX-файла\n\n")
    WORK_WITH_PATTERN = r'из ([\w]+)'
    WORK_WITH_FILES = re.findall(WORK_WITH_PATTERN, WORK_WITH_TEXT)
    WORK_WITH_AVALIBLE_CHOISES = ["1", "2", "3"]

    STATE_QUESTION_TEXT = ("Программа: Введите статус, по которому необходимо выполнить фильтрацию.\n"
                           "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n\n")

    STATE_AVALIBLE = ['EXECUTED', 'CANCELED', 'PENDING']

    def __init__(self):
        self.start()
        self.trans_data = None

    def start(self):
        if not self.is_greetings_sended:
            cprint(self.GREETINGS_TEXT, text_color='blue', text_style='curve')
            self.is_greetings_sended = True

        cprint(self.WORK_WITH_TEXT, text_style='bold')
        mode_user_input = input(self.USER)
        self.get_work_extension(mode_user_input)

    def get_work_extension(self, user_input):
        if user_input not in self.WORK_WITH_AVALIBLE_CHOISES:
            cprint('\nОШИБКА: Введите пункт ТОЛЬКО из представленых.\n', text_color='red', text_style='bold')
            return self.start()

        user_input_index = int(user_input) - 1
        choosed_file_extention = self.WORK_WITH_FILES[user_input_index]
        file_name = f'operations.{choosed_file_extention.lower()}'
        choosed_file_path = os.path.join(DATA_DIR, file_name)
        self.trans_data = get_transactions_list_from_file(choosed_file_path)

        cprint(f"\nПрограмма: Выбрана работа с данными из {choosed_file_extention} файла\n", text_color='green')

        self.filter_by_state()

    def filter_by_state(self):

        while True:
            cprint(self.STATE_QUESTION_TEXT, text_style='bold')
            filter_user_input = input(self.USER)

            if filter_user_input.upper() in self.STATE_AVALIBLE:
                break

            cprint(f"\nОШИБКА: Статус операции \"{filter_user_input}\" недоступен.\n", text_color='red', text_style='bold')








def main():
    """Главная функция для предоставления интерфэйса для работы через консоль"""
    UserInterface()


if __name__ == "__main__":
    main()