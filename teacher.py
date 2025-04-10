import tkinter as tk
from tkinter import ttk, simpledialog
import requests


API_URL = "http://127.0.0.1:8000/teachers/"

def fetch_teachers(tree):
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
                user["vk"]
            ))

    except Exception as e:
        print(f"Ошибка при получении данных: {e}")

def create_teacher(tree):
    # Создаем основное окно
    window = tk.Tk()
    window.title("Создание учителя")

    # Словарь для хранения данных учителя
    teacher_data = {}

    # Настройка меток и полей ввода
    fields = [
        ("Имя", "name"),
        ("Полное имя", "fullname"),
        ("Логин", "login"),
        ("Пароль", "password"),
        ("VK", "vk"),
        ("Gmail", "gmail"),
    ]

    entries = {}

    # Размещаем метки и поля ввода
    for idx, (label, field) in enumerate(fields):
        tk.Label(window, text=label).grid(row=idx, column=0, pady=5, padx=10)
        entry = tk.Entry(window)
        entry.grid(row=idx, column=1, pady=5, padx=10)
        entries[field] = entry

    # Статическое поле для 'role'
    teacher_data["role"] = "teacher"  # Устанавливаем значение для поля 'role'

    def submit():
        # Заполняем данные из полей
        for field, entry in entries.items():
            teacher_data[field] = entry.get()


        if all(teacher_data.values()):
            try:
                response = requests.post(API_URL, json=teacher_data)
                if response.status_code in [200, 201]:  # Добавляем 200 для успешного ответа
                    print("Учитель успешно создан")
                    print(response.json())  # Показываем полный ответ сервера
                    window.destroy()  # Закрываем окно после успешного добавления
                    fetch_teachers(tree)
                else:
                   print(f"Ошибка при создании учителя: {response.json()}")
            except Exception as e:
                print(f"Ошибка: {e}")
        else:
            print("Не все данные введены")

    # Кнопка для отправки данных
    submit_button = tk.Button(window, text="Создать учителя", command=submit)
    submit_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

    # Запускаем цикл обработки событий окна
    window.mainloop()
    


def edit_teacher(tree):
    selected_item = tree.selection()
    if selected_item:
        teacher_id = tree.item(selected_item[0])["values"][0]
        try:
            response = requests.get(f"{API_URL}{teacher_id}/")
            teacher = response.json()
            user = teacher.get('user', {})

            if not user:
                print(f"Ошибка: пользователь не найден в данных: {teacher}")
                return

            # Создаем окно для редактирования
            window = tk.Tk()
            window.title("Редактирование учителя")

            # Словарь для хранения данных учителя
            teacher_data = {}

            # Поля ввода
            fields = [
                ("Имя", "name"),
                ("Полное имя", "fullname"),
                ("Логин", "login"),
                ("Пароль", "password"),
                ("VK", "vk"),
                ("Gmail", "gmail"),
            ]

            entries = {}

            # Заполняем поля ввода значениями из существующих данных учителя
            for idx, (label, field) in enumerate(fields):
                tk.Label(window, text=label).grid(row=idx, column=0, pady=5, padx=10)
                entry = tk.Entry(window)
                entry.grid(row=idx, column=1, pady=5, padx=10)

                if field != "password":  # Не заполняем поле пароля значением с сервера
                    if field in user:
                        entry.insert(0, user[field])  # Вставляем существующие значения
                entries[field] = entry
            # Статическое поле для 'role'
            teacher_data["role"] = "teacher"  # Устанавливаем значение для поля 'role'

            def submit():
                # Заполняем данные из полей
                for field, entry in entries.items():
                    teacher_data[field] = entry.get()


                if teacher_data["password"] == "":
                    del teacher_data["password"]  # Если пароль пустой, не отправляем его

                if all(teacher_data.values()):
                    try:
                        response = requests.put(f"{API_URL}{teacher_id}/", json=teacher_data)
                        if response.status_code == 200:
                            print("Учитель успешно обновлен")
                            window.destroy()  # Закрываем окно после успешного обновления
                            fetch_teachers(tree)
                        else:
                            print(f"Ошибка при обновлении учителя: {response.json()}")
                    except Exception as e:
                        print(f"Ошибка: {e}")
                else:
                    print("Не все данные введены")

            # Кнопка для отправки данных
            submit_button = tk.Button(window, text="Обновить учителя", command=submit)
            submit_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

            # Запускаем цикл обработки событий окна
            window.mainloop()

        except Exception as e:
            print(f"Ошибка при получении данных учителя: {e}")
    else:
        print("Не выбран студент для редактирования")




def delete_teacher(tree):
    selected_item = tree.selection()
    if selected_item:
        teacher_id = tree.item(selected_item[0])["values"][0]
        try:
            response = requests.delete(f"{API_URL}{teacher_id}/")
            if response.status_code in [200, 201]:
                print("Учитель удален")
                fetch_teachers(tree)  # Обновляем таблицу
            else:
                print("Ошибка при удалении учителя")
        except Exception as e:
            print(f"Ошибка: {e}")
    else:
        print("Не выбран студент для удаления")




