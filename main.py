import re

from src.design import cprint


class UserInterface:
    is_greetings_sended = False

    USER = "Пользователь: "

    GREETINGS_TEXT = ("Программа: Привет!\n"
                      "Добро пожаловать в программу работы с банковскими транзакциями.\n"
                      "Выберите необходимый пункт меню:\n")

    WORK_WITH_TEXT = ("\n1. Получить информацию о транзакциях из JSON-файла\n"
                      "2. Получить информацию о транзакциях из CSV-файла\n"
                      "3. Получить информацию о транзакциях из XLSX-файла\n\n")
    WORK_WITH_PATTERN = r'из ([\w-]+)'
    WORK_WITH_FILES = re.findall(WORK_WITH_PATTERN, WORK_WITH_TEXT)
    WORK_WITH_AVALIBLE_CHOISES = ["1", "2", "3"]

    def __init__(self):
        self.start()

    def start(self):
        if not self.is_greetings_sended:
            cprint(self.GREETINGS_TEXT, text_color='blue', text_style='curve')
            self.is_greetings_sended = True

        cprint(self.WORK_WITH_TEXT, text_style='bold')
        self.get_work_extension(input(self.USER))

    def get_work_extension(self, user_input):
        if user_input not in self.WORK_WITH_AVALIBLE_CHOISES:
            cprint('Введите пункт ТОЛЬКО из представленых.', text_color='red', text_style='bold')
            self.start()

        user_input_index = int(user_input) - 1
        choosed_file = self.WORK_WITH_FILES[user_input_index]
        cprint(f"\nВыбрана работа с данными из {choosed_file}", text_color='green')


def main():
    """Главная функция для предоставления интерфэйса для работы через консоль"""
    UserInterface()


if __name__ == "__main__":
    main()
