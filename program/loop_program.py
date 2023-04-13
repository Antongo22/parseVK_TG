from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import graf.grafic
from graf.grafic import Window
from selenium import webdriver

window = Window()
new_folder_path = None

# Указываем путь к chromedriver.exe
driver_path = 'путь_к_файлу/chromedriver.exe'


# Создаем экземпляр класса ChromeDriver
browser = webdriver.Chrome(executable_path=driver_path)


# Класс выполнения программы
class Program:
    def open_site(self):
        import time

        # Открываем вкладку с сайтом https://vk.com/feed
        browser.get('https://vk.com/feed')

        # Ждем 30 секунд
        time.sleep(1)

        # Открываем вкладку с сайтом https://vk.com/aesthetic_tyann
        browser.execute_script(f"window.open('{graf.grafic.reference}', '_self')")
        time.sleep(10)
        # Закрываем браузер
        browser.quit()


    def ceate_folder(self, folder_name, path):  # Создание папки для скачивания
        import os
        self.folder_name = folder_name
        self.path = path
        # склеиваем название папки и путь
        new_folder_path = os.path.join(path, folder_name)

        # создаем папку с заданным именем и путем
        try:
            os.mkdir(new_folder_path)
            print(f"Папка '{folder_name}' успешно создана в папке '{path}'")
        except FileExistsError:
            print(f"Папка '{folder_name}' уже существует в папке '{path}'")
        except OSError as error:
            print(f"Не удалось создать папку '{folder_name}' в папке '{path}': {error}")

    def get_name(self):  # Получение названия группы
        import os

        # Запрашиваем у пользователя путь к папке
        folder_path = os.path.join(self.path, self.folder_name)

        # Запрашиваем у пользователя новое название для папки

        WebDriverWait(browser, 5).until(EC.presence_of_element_located(
                    (By.XPATH, "//h1[@class='page_name']")))
        new_name = browser.find_element(By.XPATH, "//h1[@class='page_name']").text
        print(new_name)

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

    def save_last_register_time(self):  # Запись в базу данных запись, с которолй началась выгрзка
        pass

    def save_meadia(self):  # Сохранение всех данных в одку папку
        pass

    def end_program(self):  # Условие и выход из программы
        pass
        # Заверщение программы