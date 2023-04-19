from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import graf.grafic
from graf.grafic import Window
from selenium import webdriver

if graf.grafic.service == 'vk':
    from vk.parser import Parser
elif graf.grafic.service == 'tg':
    from tg.parser import Parser
elif graf.grafic.service == 'fb':
    from facebook.parser import Parser

window = Window()
new_folder_path = None

# Указываем путь к chromedriver.exe
driver_path = 'путь_к_файлу/chromedriver.exe'

# Создаем экземпляр класса ChromeDriver
browser = webdriver.Chrome(executable_path=driver_path)

parser = Parser()


# Класс выполнения программы
class Program:
    def open_site(self):  # Открытие окна и вход в ВК
        parser.open_site(browser, graf)

    def ceate_folder(self, folder_name, path):  # Создание папки для скачивания
        import os
        self.folder_name = folder_name
        self.path = path
        # склеиваем название папки и путь
        global new_folder_path
        new_folder_path = os.path.join(path, folder_name)

        # создаем папку с заданным именем и путем
        try:
            os.mkdir(new_folder_path)
            print(f"Папка '{folder_name}' успешно создана в папке '{path}'")
        except FileExistsError:
            print(f"Папка '{folder_name}' уже существует в папке '{path}'")
        except OSError as error:
            print(f"Не удалось создать папку '{folder_name}' в папке '{path}': {error}")

    def create_txt(self, txt_name, path):
        global file_path
        self.txt_name = txt_name
        self.path_t = path
        import os
        # Проверяем, существует ли указанная директория
        if not os.path.exists(path):
            print(f"Директория {path} не найдена!")
            return

        # Создаем путь к файлу
        file_path = os.path.join(path, txt_name)

        # Проверяем, существует ли файл с таким именем
        if os.path.exists(file_path):
            print(f"Файл {txt_name} уже существует!")
            return

        # Создаем файл и записываем в него текст
        with open(file_path, "w") as file:
            file.write("")

        print(f"Файл {txt_name} успешно создан в директории {path}")

    def get_name(self):  # Получение названия группы
        import os

        # Проверка на то, из какого сервиса мы берём всё
        if graf.grafic.service == 'vk':
            from vk.parser import new_name
        elif graf.grafic.service == 'tg':
            from tg.parser import new_name
        elif graf.grafic.service == 'fb':
            from facebook.parser import new_name

        global new_folder_path, new_name
        new_name_txt = new_name + ".txt"

        if graf.grafic.chose_ph.get() != "none" or graf.grafic.chose_vid.get() != "none":  # Переименовывание папки в название группы
            # Запрашиваем у пользователя путь к папке
            folder_path = os.path.join(self.path, self.folder_name)

            # Получаем имя папки из полного пути
            folder_name = os.path.basename(folder_path)

            # Получаем путь к родительской папке
            parent_folder_path = os.path.dirname(folder_path)

            # Составляем новый путь к папке с новым именем
            new_folder_path = os.path.join(parent_folder_path, new_name)

            # Переименовываем папку
            os.rename(folder_path, new_folder_path)

            # Выводим сообщение об успешном переименовании папки
            print(f"Папка {folder_name} успешно переименована в {new_name}")

        if graf.grafic.chose_text.get() != "none":  # Переименовывание файла в название группы
            file_path = os.path.join(self.path_t, self.txt_name)

            # Получение имени файла из пути
            file_name = os.path.basename(file_path)

            # Получение пути к файлу без имени файла
            dir_path = os.path.dirname(file_path)

            # Составление нового пути с новым именем файла
            new_file_path = os.path.join(dir_path, new_name_txt)

            # Переименование файла
            os.rename(file_path, new_file_path)

            print(f"Файл {file_name} переименован в {new_name_txt}")

    def save_last_register_time(self):  # Запись в базу данных запись, с которолй началась выгрзка
        pass

    def save_meadia(self):  # Сохранение всех данных в одку папку
        global new_folder_path

        # Постоянное обращение к парсеру
        while True:
            if graf.grafic.chose_vid.get() == "vid":
                print("Парсинг видео")

            if graf.grafic.chose_text.get() == "text":
                print("Парсинг текста")
            if graf.grafic.chose_ph.get() == "ph":
                try:
                    parser.download_images(browser, new_folder_path)
                except Exception as e:
                    print(f"Произошла ошибка:\n{e}\n")
                    continue

    def end_program(self):  # Условие и выход из программы
        print("Парснг завершён!")
        # Заверщение программы
