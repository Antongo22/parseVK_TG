from tkinter import *
from tkinter import filedialog
import tkinter as tk
import re
import requests

selected_folder_path = None  # переменная пути к файлу, куда будет происходить выгрузка
reference = None  # переменная для хранения ссылки на сайт
service = None  # переменная для определения типа сервиса
flag_save = False
chose_ph = None
chose_vid = None
chose_text = None


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

            if chose_ph.get() != "ph" and chose_vid.get() != "vid" and chose_text.get() != "text" or selected_folder_path == None:  # Условия для дебилов
                print("Нет инфы")
                self.error()
                return

            else:
                from program.loop_program import Program
                prog = Program()

                if chose_ph.get() != "none" or chose_vid.get() != "none":
                    prog.ceate_folder("тестовая папка", selected_folder_path)
                if chose_text.get() != "none":
                    prog.create_txt("текстовый файл", selected_folder_path)

                prog.open_site()
                print("Сайт открыт")
                prog.get_name()
                # prog.save_last_register_time()
                prog.save_meadia()
                self.end()

        def done_save(service, reference):  # подтверждение того, что сайт нормальный и можно запускать
            try:
                response = requests.get(reference)  # HTML код
                print("Cервис - " + service)
                print(reference)
                # print(response.text) # вывод кода
                print("\nДанные сайта успешно получены!\n")
                save_button = tk.Button(text="Запустить", command=but_start)
                save_button.grid(row=4, column=1, sticky="se", padx=0, pady=0)

                show_flag()

            except:
                print("Это не подходящая ссылка!\nЕсли вы хотите использовать facebook, не забудьте включить VPN!")
                self.error()

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

            elif re.search("facebook", reference):
                service = "fb"

            else:
                print("Ссылка не содержит vk/facebook или telegram/tg")
                self.error_s()
                return

            done_save(service, reference)

        # Открытие главного окна
        window = Tk()
        window.title("Парсер ВК и ТГ")
        window.geometry('690x240')

        # Текстовое окно
        label = Label(text=" Введите путь к  папке, куда будем выгружат:")
        label.grid(row=0, column=0, sticky="sw")

        # Кнопка, открывающая путь к папке
        open_button = tk.Button(text="Открыть", command=open_folder_dialog)
        open_button.grid(row=0, column=1)

        # Текстовое окно
        label = Label(text=" Вставьте ссылку на группу:")
        label.grid(row=1, column=0, sticky="sw")

        # Поле для ссылки
        message_text = Text(window, width=52, height=1, wrap=WORD)
        message_text.grid(row=1, column=1)

        def show_flag():
            print("Флаг фото: ", chose_ph.get())
            print("Флаг видео: ", chose_vid.get())
            print("Флаг текста: ", chose_text.get())

        # Выбор того, что скачиваем

        global chose_ph
        global chose_vid
        global chose_text

        chose_ph = tk.StringVar()
        chose_ph.set("none")
        chose_vid = tk.StringVar()
        chose_vid.set("none")
        chose_text = tk.StringVar()
        chose_text.set("none")

        save_ph = tk.Checkbutton(window, text="Скачивать фото", variable=chose_ph, onvalue="ph", offvalue="none")
        save_ph.grid(row=2, column=0, sticky="nw")

        save_vid = tk.Checkbutton(window, text="Скачивать видео", variable=chose_vid, onvalue="vid", offvalue="none")
        save_vid.grid(row=3, column=0, sticky="w")

        save_text = tk.Checkbutton(window, text="Скачивать текст", variable=chose_text, onvalue="text", offvalue="none")
        save_text.grid(row=4, column=0, sticky="sw")

        save_button = tk.Button(text="Сохранить", command=save)
        save_button.grid(row=3, column=1, padx=0, pady=10)

        window.mainloop()

    def end(self):  # Функция, сигнализирующая о конце программы
        window = Tk()
        window.title("Парсер ВК и ТГ")
        window.geometry('250x50')

        # Вывод текста в текстовое окно
        info = tk.Label(window, text=f"Программа завершила свою работу!")
        info.grid()
        window.mainloop()

    def error(self):  # Окно ошибки
        window = Tk()
        window.title("Парсер ВК и ТГ")
        window.geometry('300x60')

        # Вывод текста в текстовое окно
        info = tk.Label(window, text=f"Вы ввели не корректныйе или не все данные!\nПовторите попытку!")
        info.grid(row=0, column=0, sticky="n")

        ok_button = tk.Button(window, text="   Ок   ", command=window.destroy)
        ok_button.grid(row=1, column=0, sticky="se")

        window.mainloop()

    def error_s(self):  # Окно ошибки о том, что сервис не корректный
        window = Tk()
        window.title("Парсер ВК и ТГ")
        window.geometry('300x60')

        # Вывод текста в текстовое окно
        info = tk.Label(window, text=f"Ссылка не содержит vk/facebook или telegram/tg\nПовторите попытку!")
        info.grid(row=0, column=0, sticky="n")

        ok_button = tk.Button(window, text="   Ок   ", command=window.destroy)
        ok_button.grid(row=1, column=0, sticky="se")

        window.mainloop()