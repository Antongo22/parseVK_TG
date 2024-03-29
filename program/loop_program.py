import time

import graf.grafic
from selenium import webdriver
import os

import vk.parser

# Создаём экземпляр класса Window
window = graf.grafic.Window()

# Определяем из каково файла брать класс Parser
if graf.grafic.service == 'vk':
    if graf.grafic.chat == "im":
        from vk.parser import Parser_ls, count_p, count_t, count_v
    elif graf.grafic.chat == "wall":
        from vk.parser import Parser_wall, count_p, count_t, count_v

elif graf.grafic.service == 'tg':
    from tg.parser import Parser, count_p, count_t, count_v
elif graf.grafic.service == 'fb':
    from facebook.parser import Parser, count_p, count_t, count_v

# создаё экземпляр класса Parser
if graf.grafic.service == 'vk':
    if graf.grafic.chat == "im":
        parser = Parser_ls()
    elif graf.grafic.chat == "wall":
        parser = Parser_wall()

if graf.grafic.service == 'fb':
    parser = Parser()

if graf.grafic.service == 'tg':
    parser = Parser()

new_folder_path = None  # Переменная, которая хранит путь к папке сохранения

new_file_path = None  # Переменная, которая хранит путь к файлу сохранения

file = None  # Переменная для файла

new_name = None  # переменная нового имени для файла

error_t = ""  # переменна для хранения ошибки


# Класс выполнения программы
class Program:

    def open_site(self, browser):  # Открытие окна и вход в ВК
        parser.open_site(browser, graf)
        print()

    def ceate_folder(self, folder_name, path):  # Создание папки для скачивания
        self.__path = path
        self.__folder_name = folder_name
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
            window.error(f"Не удалось создать папку '{folder_name}' в папке '{path}': {error}")

    def create_txt(self, txt_name, path):

        global file  # Переменная для файла

        global file_path  # Переменная для хранения пути к файлам

        # Проверяем, существует ли указанная директория
        if not os.path.exists(path):
            print(f"Директория {path} не найдена!\n")
            window.error(f"Директория {path} не найдена!")
            return

        # Создаем путь к файлу
        file_path = os.path.join(path, txt_name)

        try:
            # Проверяем, существует ли файл с таким именем
            if os.path.exists(file_path):
                print(f"Файл {txt_name} уже существует!\n")
                window.error(f"Файл {txt_name} уже существует!")
                return

            # Создаем файл и записываем в него текст
            with open(file_path, "w") as file:
                file.write("")
        except:
            pass

        print(f"Файл {txt_name} успешно создан в директории {path}\n")

    def get_name(self):  # Получение названия группы

        # Проверка на то, из какого сервиса мы берём всё
        if graf.grafic.service == 'vk':
            from vk.parser import new_name
        elif graf.grafic.service == 'tg':
            from tg.parser import new_name
        elif graf.grafic.service == 'fb':
            from facebook.parser import new_name

        global new_name
        print("Имя " + new_name)

        # Если в тескте есть мешающие символы, они будут удалены
        new_text = ""
        for char in new_name:
            if not char.isalpha() and not char.isdigit() and char != " ":
                new_text += "_"
            else:
                new_text += char
        new_name = new_text

        global new_folder_path, new_file_path, folder_path
        __new_name_txt = new_name + ".txt"

        if graf.grafic.chose_ph.get() != "none" or graf.grafic.chose_vid.get() != "none":  # Переименовывание папки в название группы
            try:
                # Запрашиваем у пользователя путь к папке
                folder_path = os.path.join(self.__path, self.__folder_name)

                # Получаем имя папки из полного пути
                __folder_name = os.path.basename(folder_path)

                # Получаем путь к родительской папке
                __parent_folder_path = os.path.dirname(folder_path)

                # Составляем новый путь к папке с новым именем
                new_folder_path = os.path.join(__parent_folder_path, new_name)

                # Переименовываем папку
                os.rename(folder_path, new_folder_path)

                # Выводим сообщение об успешном переименовании папки
                print(f"Папка {__folder_name} успешно переименована в {new_name}")
            except:
                print(
                    f"Папка {new_name} уже существует! Всё будет перезаписано в старую папку, а тестовая будет удалена!")

                # Удаление тестовой папки
                try:
                    os.rmdir(folder_path)
                    print(f"Папка '{folder_path}' успешно удалена.")
                except OSError as e:
                    print(f"Удаление папки '{folder_path}' не удалось: {e}")

        if graf.grafic.chose_text.get() != "none":  # Переименовывание файла в название группы

            try:
                # Получение имени файла из пути
                __file_name = os.path.basename(file_path)

                # Получение пути к файлу без имени файла
                __dir_path = os.path.dirname(file_path)

                # Составление нового пути с новым именем файла
                new_file_path = os.path.join(__dir_path, __new_name_txt)

                # Переименование файла
                os.rename(file_path, new_file_path)

                print(f"Файл {__file_name} переименован в {__new_name_txt}")
            except:
                print(f"Файл {__new_name_txt} уже существует!")

                # Удаление тестовой папки
                try:
                    os.remove(file_path)
                    print(f"Файл '{file_path}' успешно удален.")
                except OSError as e:
                    print(f"Удаление файла '{file_path}' не удалось: {e}")

    def save_last_register_time(self):  # Запись в базу данных запись, с которолй началась выгрзка
        pass

    def save_meadia(self, browser):  # Сохранение всех данных в одку папку
        global new_folder_path, error_t
        end = 0
        error = 0

        # Постоянное обращение к парсеру
        while True:

            # Парсинг фото
            if graf.grafic.chose_ph.get() == "ph":
                try:
                    parser.download_images(browser, new_folder_path)
                    print("Сессия парсинга фото завершена! \n")
                except Exception as e:
                    print(f"\nПроизошла ошибка в фото:\n{e}\n\n")
                    error += 1
                    continue

            # Парсинг текста
            if graf.grafic.chose_text.get() == "text":
                try:
                    parser.download_text(browser, new_file_path)
                    print("Сессия парсинга текста завершена!\n")
                except Exception as e:
                    print(f"\nПроизошла ошибка в тексте:\n{e}\n\n")

                    error += 1
                    continue

            # Парсинг видео
            if graf.grafic.chose_vid.get() == "vid":
                parser.download_videos(browser, new_folder_path)
                print("Сессия парсинга видео завершена!\n")

            end_of_page = browser.execute_script(
                "return (window.innerHeight + window.pageYOffset) >= document.body.offsetHeight")

            if graf.grafic.service != 'fb':
                # Если нет данных, то он останавливает
                if error == 35:
                    error_t = "Произошла ошибка, возможно вы закрыли браузер.\nПовторите попытку!"
                    break

                # Если коннец страницы, то завершает
                if end_of_page:
                    end += 1
                    time.sleep(20)
                    if end >= 10:
                        break
            if end_of_page:
                end += 1
                time.sleep(20)
                if end >= 20:
                    break

    def end_program(self, browser):  # Условие и выход из программы
        # Определяем из каково файла брать класс Parser
        if graf.grafic.service == 'vk':
            from vk.parser import count_p, count_t, count_v
        elif graf.grafic.service == 'tg':
            from tg.parser import count_p, count_t, count_v
        elif graf.grafic.service == 'fb':
            from facebook.parser import count_p, count_t, count_v

        global count_v, count_t, count_p
        print("Парснг завершён!")

        if graf.grafic.chose_exit.get() == "exit":
            parser.end(browser)

        if error_t == "":
            text = f"Программа завершила свою работу\nВсего обработанно:\n {count_p} фото, {count_v} видео и {count_t} тексовых постов"
        else:
            text = error_t

        print(text)
        return text
