import time
from tkinter import *
from tkinter import filedialog
import tkinter as tk
import re
import requests
from selenium import webdriver

selected_folder_path = None  # переменная пути к файлу, куда будет происходить выгрузка
reference = None  # переменная для хранения ссылки на сайт
service = None  # переменная для определения типа сервиса
chose_ph = None  # переменная для состояния данных о фото
chose_vid = None  # переменная для состояния данных о видео
chose_text = None  # переменная для состояния данных о текст
chose_exit = None


# Класс графики
class Window:

    def start(self):  # Начальный экран бота

        def open_folder_dialog():  # Выбор папки, куда будем сохранять
            global selected_folder_path
            __folder_path = filedialog.askdirectory()

            if __folder_path:
                selected_folder_path = __folder_path
                print(selected_folder_path)
            else:
                selected_folder_path = None

        def but_start():  # Запуск бота
            global browser
            # Обработка того, что пользователь ввёл не все данные
            if chose_ph.get() != "ph" and chose_vid.get() != "vid" and chose_text.get() != "text" or selected_folder_path == None:  # Условия для дебилов
                print("Нет инфы")
                self.error("Вы не указали что скачивать или не указали папку!")
                return

            # Если всё хорошо, то программа запустится
            else:
                try:
                    # Указываем путь к chromedriver.exe
                    driver_path = 'путь_к_файлу/chromedriver.exe'
                    # Создаем экземпляр класса ChromeDriver
                    browser = webdriver.Chrome(executable_path=driver_path)

                    from program.loop_program import Program

                    # Создание экземпяра класса
                    prog = Program()

                    # Создание разных папок/файлов в зависимости от того, что скачиваем
                    if chose_ph.get() != "none" or chose_vid.get() != "none":
                        prog.ceate_folder("тестовая папка", selected_folder_path)
                    if chose_text.get() != "none":
                        prog.create_txt("тестовый файл", selected_folder_path)

                    prog.open_site(browser)
                    print("Сайт открыт")

                    # Переименовывание фалоов
                    prog.get_name()

                    # Запись в БД данных о последнем посте
                    # prog.save_last_register_time()

                    # Вызов сохранения данных
                    prog.save_meadia(browser)

                    # Уведомление о концце программы
                    self.end(prog.end_program(browser))

                except Exception as e:
                    print("Ошибка:\n" + e)
                    self.error("Произошла ошибка во время парсинга!\nПерезапустите программу!")
                    __window.destroy()

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
                self.error("Это не подходящая ссылка!\nЕсли вы хотите использовать facebook, не забудьте включить VPN!")

        def save():  # Сохранение ссылки
            global service
            global reference

            # Расшифровка ссылкии
            reference = __message_text.get("1.0", "end-1c")

            # Обнаружение в ссылке сервиса
            if re.search("vk", reference):
                service = "vk"

            elif re.search("telegram|tg", reference):
                service = "tg"

            elif re.search("facebook", reference):
                service = "fb"

            else:
                print("Ссылка не содержит vk/facebook или telegram/tg")
                self.error("Ссылка не содержит vk/facebook или telegram/tg")
                return

            done_save(service, reference)

        # Открытие главного окна
        __window = Tk()
        __window.title("Парсер ВК и ТГ")
        __window.geometry('690x240')

        # Текстовое окно
        __label_info = Label(text=" Введите путь к  папке, куда будем выгружат:")
        __label_info.grid(row=0, column=0, sticky="sw")

        # Кнопка, открывающая путь к папке
        __open_button = tk.Button(text="Открыть", command=open_folder_dialog)
        __open_button.grid(row=0, column=1)

        # Текстовое окно
        __label_reference = Label(text=" Вставьте ссылку на группу:")
        __label_reference.grid(row=1, column=0, sticky="sw")

        # Поле для ссылки
        __message_text = Text(__window, width=52, height=1, wrap=WORD)
        __message_text.grid(row=1, column=1)

        def show_flag():  # Показвает состояния флагов
            print("Флаг фото: ", chose_ph.get())
            print("Флаг видео: ", chose_vid.get())
            print("Флаг текста: ", chose_text.get())
            print("Флаг выхода: ", chose_exit.get())
            print()

        # Выбор того, что скачиваем
        global chose_ph  # индикатор фото
        global chose_vid  # индикатор видео
        global chose_text  # индикатор текста
        global chose_exit # Индикатор закрытия браузера

        # Создаём чекбоксы и задаём им отключённое значение
        chose_ph = tk.StringVar()
        chose_ph.set("none")
        chose_vid = tk.StringVar()
        chose_vid.set("none")
        chose_text = tk.StringVar()
        chose_text.set("none")
        chose_exit = tk.StringVar()
        chose_exit.set("none")


        # Чекбокс фото
        __save_ph = tk.Checkbutton(__window, text="Скачивать фото", variable=chose_ph, onvalue="ph", offvalue="none")
        __save_ph.grid(row=2, column=0, sticky="nw")

        # Чекбокс видео
        __save_vid = tk.Checkbutton(__window, text="Скачивать видео", variable=chose_vid, onvalue="vid",
                                    offvalue="none")
        __save_vid.grid(row=3, column=0, sticky="w")

        # Чекбокс текста
        __save_text = tk.Checkbutton(__window, text="Скачивать текст", variable=chose_text, onvalue="text",
                                     offvalue="none")
        __save_text.grid(row=4, column=0, sticky="sw")

        # Автовыход браузера
        __exit = tk.Checkbutton(__window, text="Автоматически закрывать браузер", variable=chose_exit, onvalue="exit",
                                    offvalue="none")
        __exit.grid(row=5, column=0, sticky="w")

        # Кнопка сохранения
        __save_button = tk.Button(text="Сохранить", command=save)
        __save_button.grid(row=3, column=1, padx=0, pady=10)

        # Обработка окна
        __window.mainloop()

    def end(self, text):  # Функция, сигнализирующая о конце программы
        # Откртие окна конца
        __window_ebd = Tk()
        __window_ebd.title("Парсер ВК и ТГ")

        # Вывод текста в текстовое окно
        __info = tk.Label(__window_ebd, text=f"{text}")
        __info.grid()

        # Кнопка для выхода
        __ok_button = tk.Button(__window_ebd, text="      Ок      ", command=__window_ebd.destroy)
        __ok_button.grid(row=1, column=0, sticky="se")

        # Обработка окна
        __window_ebd.mainloop()

    def error(self, text):  # Окно ошибки

        # Откртие окна ошибки
        __window_error = Tk()
        __window_error.title("Парсер ВК и ТГ")

        # Вывод текста в текстовое окно
        __info = tk.Label(__window_error, text=text)
        __info.grid(row=0, column=0, sticky="n")

        # Кнопка для выхода
        __ok_button = tk.Button(__window_error, text="      Ок      ", command=__window_error.destroy)
        __ok_button.grid(row=1, column=0, sticky="se")

        # Обработка окна
        __window_error.mainloop()
