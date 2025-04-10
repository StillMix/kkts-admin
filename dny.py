import tkinter as tk
from tkinter import ttk, simpledialog
import requests


API_URL = "http://127.0.0.1:8000/lesson/"

def fetch_days(tree):
    # Очистка таблицы перед обновлением
    for row in tree.get_children():
        tree.delete(row)

    try:
        response = requests.get(API_URL)
        data = response.json()
        for user in data.get("lessons", []):
            tree.insert("", "end", values=(
                user["id"],
                user["date"]
            ))

    except Exception as e:
        print(f"Ошибка при получении данных: {e}")

def create_day(tree):
    # Создаем основное окно
    window = tk.Tk()
    window.title("Создание дняа")

    # Словарь для хранения данных дняа
    day_data = {}

    # Настройка меток и полей ввода
    fields = [
        ("Дата", "date")
    ]

    entries = {}

    # Размещаем метки и поля ввода
    for idx, (label, field) in enumerate(fields):
        tk.Label(window, text=label).grid(row=idx, column=0, pady=5, padx=10)
        entry = tk.Entry(window)
        entry.grid(row=idx, column=1, pady=5, padx=10)
        entries[field] = entry


    def submit():
        # Заполняем данные из полей
        for field, entry in entries.items():
            day_data[field] = entry.get()

        if all(day_data.values()):
            try:
                response = requests.post(API_URL, json=day_data)
                if response.status_code in [200, 201]:  # Добавляем 200 для успешного ответа
                    print("День успешно создан")
                    print(response.json())  # Показываем полный ответ сервера
                    window.destroy()  # Закрываем окно после успешного добавления
                    fetch_days(tree)
                else:
                   print(f"Ошибка при создании дня: {response.json()}")
            except Exception as e:
                print(f"Ошибка: {e}")
        else:
            print("Не все данные введены")

    # Кнопка для отправки данных
    submit_button = tk.Button(window, text="Создание дня", command=submit)
    submit_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

    # Запускаем цикл обработки событий окна
    window.mainloop()
    


