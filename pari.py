import tkinter as tk
from tkinter import ttk, simpledialog, colorchooser
import requests


API_URL = "http://127.0.0.1:8000/lesson/{day.id}/session/"

def fetch_teachers_combobox():
    try:
        response = requests.get("http://127.0.0.1:8000/teachers")
        data = response.json()
        teachers = data.get("users", [])
        teacher_names = [teacher["name"] for teacher in teachers]
        teacher_ids = {teacher["name"]: teacher["id"] for teacher in teachers}
        return teacher_names, teacher_ids
    except Exception as e:
        print(f"Ошибка при получении учителей: {e}")
        return [], {}




def fetch_paris(tree, day_id: int):
    # Очистка таблицы перед обновлением
    for row in tree.get_children():
        tree.delete(row)

    try:
        response = requests.get(f"http://127.0.0.1:8000/lesson/{day_id}/session/")  # Используем day_id для запроса
        data = response.json()

        for pari in data.get("session", []):  # Поменял "users" на "sessions"

            tree.insert("", "end", values=(
                pari["id"],
                pari["name"],
                pari["group"],
                pari["teacher"],
                pari["teacher2"],
                pari["start"],
                pari["end"],
                pari["clases"],
                pari["adress"],
                pari["color"]
            ))

    except Exception as e:
        print(f"Ошибка при получении данных: {e}")

def choose_color():
    """Открывает диалог выбора цвета и возвращает выбранный цвет в формате HEX"""
    color = colorchooser.askcolor()[1]  # Второй элемент возвращает HEX цвет
    return color

def create_pari(tree, day_id):
    # Создаем основное окно
    window = tk.Tk()
    window.title("Создание пары")

    # Словарь для хранения данных пары
    pari_data = {}

    # Получаем список учителей
    teacher_names, teacher_ids = fetch_teachers_combobox()

    # Настройка меток и полей ввода
    fields = [
        ("Имя", "name"),
        ("Группа", "group"),
        ("Начало", "start"),
        ("Конец", "end"),
        ("Класс", "clases"),
        ("Адрес", "adress"),
        ("Цвет", "color")  # Добавлено поле для цвета
    ]

    entries = {}

    # Размещаем метки и поля ввода
    for idx, (label, field) in enumerate(fields):
        tk.Label(window, text=label).grid(row=idx, column=0, pady=5, padx=10)
        entry = tk.Entry(window)
        entry.grid(row=idx, column=1, pady=5, padx=10)
        entries[field] = entry

    # Добавляем комбинированный список для выбора учителей
    tk.Label(window, text="Выберите учителя 1").grid(row=len(fields), column=0, pady=5, padx=10)
    teacher_combobox1 = ttk.Combobox(window, values=teacher_names)
    teacher_combobox1.grid(row=len(fields), column=1, pady=5, padx=10)

    tk.Label(window, text="Выберите учителя 2 (необязательно)").grid(row=len(fields) + 1, column=0, pady=5, padx=10)
    teacher_combobox2 = ttk.Combobox(window, values=teacher_names)
    teacher_combobox2.grid(row=len(fields) + 1, column=1, pady=5, padx=10)

    # Кнопка для выбора цвета
    def pick_color():
        color = choose_color()
        if color:  # Если цвет выбран
            entries['color'].delete(0, tk.END)  # Очищаем поле ввода
            entries['color'].insert(0, color)  # Вставляем выбранный цвет в поле

    color_button = tk.Button(window, text="Выбрать цвет", command=pick_color)
    color_button.grid(row=len(fields) + 2, column=0, columnspan=2, pady=10)

    def submit():
        # Заполняем данные из полей
        for field, entry in entries.items():
            pari_data[field] = entry.get()

        # Получаем ID учителей из combobox
        teacher1_name = teacher_combobox1.get()
        teacher2_name = teacher_combobox2.get()

        if teacher1_name in teacher_ids:
            pari_data["teacher"] = str(teacher_ids[teacher1_name])  # Передаем как строку

        # Если второй учитель выбран, добавляем его ID, если нет — отправляем пустую строку
        if teacher2_name in teacher_ids:
            pari_data["teacher2"] = str(teacher_ids[teacher2_name])  # Передаем как строку
        else:
            pari_data["teacher2"] = ""  # Пустая строка, если учитель не выбран

        # Проверяем, что все обязательные поля заполнены
        if all(pari_data.get(field) for field in ["name", "group", "start", "end", "clases", "adress", "color", "teacher"]):
            try:
                response = requests.post(f"http://127.0.0.1:8000/lesson/{day_id}/session/", json=pari_data)
                if response.status_code in [200, 201]:
                    print("Пара успешно создана")
                    window.destroy()  # Закрываем окно после успешного добавления
                    fetch_paris(tree, day_id)  # Обновляем список пар, передаем day_id
                else:
                    print(f"Ошибка при создании пары: {response.json()}")
            except Exception as e:
                print(f"Ошибка: {e}")
        else:
            print("Не все данные введены")

    # Кнопка для отправки данных
    submit_button = tk.Button(window, text="Создать пару", command=submit)
    submit_button.grid(row=len(fields) + 3, column=0, columnspan=2, pady=10)

    # Запускаем цикл обработки событий окна
    window.mainloop()






def edit_pari(tree, day_id):
    selected_item = tree.selection()
    if selected_item:
        pari_id = tree.item(selected_item[0])["values"][0]
        try:
            response = requests.get(f"{API_URL}{pari_id}/")
            pari = response.json()
            user = pari.get('user', {})

            if not user:
                print(f"Ошибка: пользователь не найден в данных: {pari}")
                return

            # Создаем окно для редактирования
            window = tk.Tk()
            window.title("Редактирование пары")

            # Словарь для хранения данных пары
            pari_data = {}

            # Поля ввода
            fields = [
                ("Имя", "name"),
                ("Группа", "group"),
                ("Учитель", "teacher"),
                ("Учитель", "teacher2"),
                ("Начало", "start"),
                ("Конец", "end"),
                ("Класс", "clases"),
                ("Адресс", "adress"),
                ("Цвет", "color"),  # Поле для цвета
            ]

            entries = {}

            # Заполняем поля ввода значениями из существующих данных пары
            for idx, (label, field) in enumerate(fields):
                tk.Label(window, text=label).grid(row=idx, column=0, pady=5, padx=10)
                entry = tk.Entry(window)
                entry.grid(row=idx, column=1, pady=5, padx=10)
                entries[field] = entry
                entry.insert(0, user.get(field, ""))  # Заполняем поле значением из данных

            def pick_color():
                color = choose_color()
                if color:  # Если цвет выбран
                    entries['color'].delete(0, tk.END)  # Очищаем поле ввода
                    entries['color'].insert(0, color)  # Вставляем выбранный цвет в поле

            color_button = tk.Button(window, text="Выбрать цвет", command=pick_color)
            color_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

            def submit():
                # Заполняем данные из полей
                for field, entry in entries.items():
                    pari_data[field] = entry.get()

                if all(pari_data.values()):
                    try:
                        response = requests.put(f"http://127.0.0.1:8000/lesson/{day_id}/session/{pari_id}/", json=pari_data)
                        if response.status_code == 200:
                            print("Пара успешно обновлена")
                            window.destroy()  # Закрываем окно после успешного обновления
                            fetch_paris(tree, day_id)
                        else:
                            print(f"Ошибка при обновлении пары: {response.json()}")
                    except Exception as e:
                        print(f"Ошибка: {e}")
                else:
                    print("Не все данные введены")

            # Кнопка для отправки данных
            submit_button = tk.Button(window, text="Обновить пару", command=submit)
            submit_button.grid(row=len(fields)+1, column=0, columnspan=2, pady=10)

            # Запускаем цикл обработки событий окна
            window.mainloop()

        except Exception as e:
            print(f"Ошибка при получении данных пары: {e}")
    else:
        print("Не выбран пара для редактирования")

def delete_pari(tree, day_id):
    selected_item = tree.selection()
    if selected_item:
        pari_id = tree.item(selected_item[0])["values"][0]
        try:
            response = requests.delete(f"http://127.0.0.1:8000/lesson/{day_id}/session/{pari_id}/")
            if response.status_code in [200, 201]:
                print("Пара удалена")
                fetch_paris(tree, day_id)  # Обновляем таблицу
            else:
                print("Ошибка при удалении пары")
        except Exception as e:
            print(f"Ошибка: {e}")
    else:
        print("Не выбрана пара для удаления")
