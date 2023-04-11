from tkinter import *
from tkinter import filedialog
import tkinter as tk


class Window:
    selected_folder_path = None

    def start(self):  # Начальный экран бота

        def open_folder_dialog():
            global selected_folder_path
            folder_path = filedialog.askdirectory()
            if folder_path:
                selected_folder_path = folder_path
                print(selected_folder_path)
            else:
                selected_folder_path = None

        window = Tk()
        window.title("Парсер ВК и ТГ")
        window.geometry('800x550+650+150')

        label = Label(text=" Введите путь к  папке, куда будем выгружат:                          ")
        label.grid(row=0, column=0)
        open_button = tk.Button(text="Открыть", command=open_folder_dialog)
        open_button.grid(row=0, column=1)

        label = Label(text=" Вставьте ссылку на группу:                          ")
        label.grid(row=1, column=0)
        message_text = Text(window, width=52, height=1, wrap=WORD)
        message_text.grid(row=1, column=1)
        window.mainloop()


window = Window()
window.start()
