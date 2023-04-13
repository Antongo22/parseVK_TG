from tkinter import *
from tkinter import filedialog
import tkinter as tk
import re
import requests

selected_folder_path = None  # переменная пути к файлу, куда будет происходить выгрузка
reference = None  # переменная для хранения ссылки на сайт
service = None  # переменная для определения типа сервиса


# Класс графики
class Window:

    def start(self):  # Начальный экран бота

        def open_folder_dialog():  # Выбор папки, куда будем сохранять
            global selected_folder_path
            folder_path = filedialog.askdirectory()
            if folder_path:
                selected_folder_path = folder_path
                print(selected_folder_path)
            else:
                selected_folder_path = None

        def but_start():  # Запуск бота

            from program.loop_program import Program

            prog = Program()
            prog.ceate_folder("тестовая папка", selected_folder_path)
            prog.open_site()
            prog.get_name()
            prog.save_last_register_time()
            prog.save_meadia()
            self.end()

        def done_save(service, reference):  # подтверждение того, что сайт нормальный и можно запускать
            try:
                response = requests.get(reference)  # HTML код
                print(service)
                print(reference)
                # print(response.text) # вывод кода
                print("\nДанные сайта успешно получены!")
                save_button = tk.Button(text="Запустить", command=but_start)
                save_button.grid(row=3, column=1, sticky="se", padx=0, pady=100)

            except:
                print("Это не подходящая ссылка!")

        def save():  # Сохранение ссылки
            global service
            global reference

            # Расшифровка ссылкии
            reference = message_text.get("1.0", "end-1c")

            # Обнаружение в ссылке сервиса
            if re.search("vk", reference):
                service = "vk"

            elif re.search("telegram|tg", reference):
                service = "tg"
            else:
                print("Ссылка не содержит vk или telegram/tg")
                return

            done_save(service, reference)

        window = Tk()
        window.title("Парсер ВК и ТГ")
        window.geometry('690x240')

        label = Label(text=" Введите путь к  папке, куда будем выгружат:")
        label.grid(row=0, column=0, sticky="sw")
        open_button = tk.Button(text="Открыть", command=open_folder_dialog)
        open_button.grid(row=0, column=1)

        label = Label(text=" Вставьте ссылку на группу:")
        label.grid(row=1, column=0, sticky="sw")
        message_text = Text(window, width=52, height=1, wrap=WORD)
        message_text.grid(row=1, column=1)

        save_button = tk.Button(text="Сохранить", command=save)
        save_button.grid(row=2, column=1, padx=0, pady=10)

        window.mainloop()

    def end(self):  # Функция, сигнализирующая о конце программы
        window = Tk()
        window.title("Парсер ВК и ТГ")
        window.geometry('250x50')

        # Вывод текста в текстовое окно
        info = tk.Label(window, text=f"Программа завершила свою работу!")
        info.grid()