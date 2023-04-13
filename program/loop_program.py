from graf.grafic import Window

window = Window()


# Класс выполнения программы
class Program:
    def get_name(self):  # Получение названия группы
        pass

    def ceate_folder(self, folder_name, path):  # Создание папки для скачивания
        import os

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

    def save_last_register_time(self):  # Запись в базу данных запись, с которолй началась выгрзка
        pass

    def save_meadia(self):  # Сохранение всех данных в одку папку
        pass

    def end_program(self):  # Условие и выход из программы
        pass
        # Заверщение программы



