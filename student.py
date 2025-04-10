import tkinter as tk
from tkinter import ttk, simpledialog
import requests


API_URL = "http://127.0.0.1:8000/students/"

def fetch_students(tree):
    # Очистка таблицы перед обновлением
    for row in tree.get_children():
        tree.delete(row)

    try:
        response = requests.get(API_URL)
        data = response.json()
        for user in data.get("users", []):
            tree.insert("", "end", values=(
                user["id"],
                user["name"],
                user["fullname"],
                user["login"],
                user["gmail"],
                user["group"],
                user["srbal"],
                user["vk"]
            ))

    except Exception as e:
        print(f"Ошибка при получении данных: {e}")

def create_student(tree):
    # Создаем основное окно
    window = tk.Tk()
    window.title("Создание студента")

    # Словарь для хранения данных студента
    student_data = {}

    # Настройка меток и полей ввода
    fields = [
        ("Имя", "name"),
        ("Полное имя", "fullname"),
        ("Логин", "login"),
        ("Пароль", "password"),
        ("Группа", "group"),
        ("VK", "vk"),
        ("Gmail", "gmail"),
        ("Средний балл", "srbal")
    ]

    entries = {}

    # Размещаем метки и поля ввода
    for idx, (label, field) in enumerate(fields):
        tk.Label(window, text=label).grid(row=idx, column=0, pady=5, padx=10)
        entry = tk.Entry(window)
        entry.grid(row=idx, column=1, pady=5, padx=10)
        entries[field] = entry

    # Статическое поле для 'role'
    student_data["role"] = "user"  # Устанавливаем значение для поля 'role'

    def submit():
        # Заполняем данные из полей
        for field, entry in entries.items():
            student_data[field] = entry.get()

        # Преобразуем "Средний балл" в строку
        try:
            student_data["srbal"] = str(student_data["srbal"])  # Преобразуем в строку
        except ValueError:
            print("Ошибка: Средний балл должен быть числом")
            return

        if all(student_data.values()):
            try:
                response = requests.post(API_URL, json=student_data)
                if response.status_code in [200, 201]:  # Добавляем 200 для успешного ответа
                    print("Студент успешно создан")
                    print(response.json())  # Показываем полный ответ сервера
                    window.destroy()  # Закрываем окно после успешного добавления
                    fetch_students(tree)
                else:
                   print(f"Ошибка при создании студента: {response.json()}")
            except Exception as e:
                print(f"Ошибка: {e}")
        else:
            print("Не все данные введены")

    # Кнопка для отправки данных
    submit_button = tk.Button(window, text="Создать студента", command=submit)
    submit_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

    # Запускаем цикл обработки событий окна
    window.mainloop()
    


def edit_student(tree):
    selected_item = tree.selection()
    if selected_item:
        student_id = tree.item(selected_item[0])["values"][0]
        try:
            response = requests.get(f"{API_URL}{student_id}/")
            student = response.json()
            user = student.get('user', {})

            if not user:
                print(f"Ошибка: пользователь не найден в данных: {student}")
                return

            # Создаем окно для редактирования
            window = tk.Tk()
            window.title("Редактирование студента")

            # Словарь для хранения данных студента
            student_data = {}

            # Поля ввода
            fields = [
                ("Имя", "name"),
                ("Полное имя", "fullname"),
                ("Логин", "login"),
                ("Пароль", "password"),
                ("Группа", "group"),
                ("VK", "vk"),
                ("Gmail", "gmail"),
                ("Средний балл", "srbal")
            ]

            entries = {}

            # Заполняем поля ввода значениями из существующих данных студента
            for idx, (label, field) in enumerate(fields):
                tk.Label(window, text=label).grid(row=idx, column=0, pady=5, padx=10)
                entry = tk.Entry(window)
                entry.grid(row=idx, column=1, pady=5, padx=10)

                if field != "password":  # Не заполняем поле пароля значением с сервера
                    if field in user:
                        entry.insert(0, user[field])  # Вставляем существующие значения
                entries[field] = entry
            # Статическое поле для 'role'
            student_data["role"] = "user"  # Устанавливаем значение для поля 'role'

            def submit():
                # Заполняем данные из полей
                for field, entry in entries.items():
                    student_data[field] = entry.get()

                # Преобразуем "Средний балл" в строку
                try:
                    student_data["srbal"] = str(student_data["srbal"])  # Преобразуем в строку
                except ValueError:
                    print("Ошибка: Средний балл должен быть числом")
                    return

                if student_data["password"] == "":
                    del student_data["password"]  # Если пароль пустой, не отправляем его

                if all(student_data.values()):
                    try:
                        response = requests.put(f"{API_URL}{student_id}/", json=student_data)
                        if response.status_code == 200:
                            print("Студент успешно обновлен")
                            window.destroy()  # Закрываем окно после успешного обновления
                            fetch_students(tree)
                        else:
                            print(f"Ошибка при обновлении студента: {response.json()}")
                    except Exception as e:
                        print(f"Ошибка: {e}")
                else:
                    print("Не все данные введены")

            # Кнопка для отправки данных
            submit_button = tk.Button(window, text="Обновить студента", command=submit)
            submit_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

            # Запускаем цикл обработки событий окна
            window.mainloop()

        except Exception as e:
            print(f"Ошибка при получении данных студента: {e}")
    else:
        print("Не выбран студент для редактирования")




def delete_student(tree):
    selected_item = tree.selection()
    if selected_item:
        student_id = tree.item(selected_item[0])["values"][0]
        try:
            response = requests.delete(f"{API_URL}{student_id}/")
            if response.status_code in [200, 201]:
                print("Студент удален")
                fetch_students(tree)  # Обновляем таблицу
            else:
                print("Ошибка при удалении студента")
        except Exception as e:
            print(f"Ошибка: {e}")
    else:
        print("Не выбран студент для удаления")




