import tkinter as tk
from tkinter import ttk
from student import fetch_students, create_student, edit_student, delete_student
from teacher import fetch_teachers, create_teacher, edit_teacher, delete_teacher
from dny import fetch_days , create_day
from pari import fetch_paris, create_pari, edit_pari, delete_pari

def to_student():
    window.withdraw()  # Скрываем главное окно
    open_student_window()  # Открываем окно студентов

def to_pari(tree, day_window):
    # Получаем выбранный день (id)
    selected_item = tree.selection()
    if selected_item:
        selected_item_id = selected_item[0]  # Получаем ID выбранного элемента
        day_name = tree.item(selected_item_id)["values"][1]  # Получаем название дня
        day_id = tree.item(selected_item_id)["values"][0]  # Получаем ID дня
        window.withdraw()  # Скрываем главное окно
        open_pari_window(day_id, day_name)  # Открываем окно с парами
    else:
        print("Выберите день для открытия пар")


def to_teacher():
    window.withdraw()  # Скрываем главное окно
    open_teacher_window()  # Открываем окно учителей

def to_day():
    window.withdraw()  # Скрываем главное окно
    open_day_window()  # Открываем окно учителей

def to_main(window_to_close):
    window_to_close.destroy()  # Закрываем окно (студентов или учителей)
    window.deiconify()  # Показываем главное окно


def open_pari_window(day_id, day_name):

    pari_window = tk.Toplevel(window)
    pari_window.title(f"Пары для дня {day_id}")
    pari_window.geometry("800x400")

    label = tk.Label(pari_window, text=f"Список пар {day_name}", font=("Arial", 14))
    label.pack(pady=10)


    columns = ("id", "name", "group", "teacher", "teacher2", "start", "end", "clases", "adress", "color")
    tree = ttk.Treeview(pari_window, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=100, anchor="center")

    tree.pack(fill=tk.BOTH, expand=True)


    button_frame = tk.Frame(pari_window)
    button_frame.pack(pady=10)

    btn_refresh = tk.Button(button_frame, text="Обновить таблицу", command=lambda: fetch_paris(tree, day_id))
    btn_refresh.grid(row=0, column=0, padx=10)

    btn_create = tk.Button(button_frame, text="Создать пару", command=lambda: create_pari(tree, day_id))
    btn_create.grid(row=0, column=1, padx=10)

    btn_edit = tk.Button(button_frame, text="Редактировать пару", command=lambda: edit_pari(tree, day_id))
    btn_edit.grid(row=0, column=2, padx=10)

    btn_delete = tk.Button(button_frame, text="Удалить пару", command=lambda: delete_pari(tree, day_id))
    btn_delete.grid(row=0, column=3, padx=10)

    fetch_paris(tree, day_id)

    pari_window.mainloop()

def open_day_window():
    # Создаем новое окно дней поверх основного окна
    day_window = tk.Toplevel(window)
    day_window.title("Дни")
    day_window.geometry("800x400")

    # Заголовок
    label = tk.Label(day_window, text="Список Дней", font=("Arial", 14))
    label.pack(pady=10)

    # Создание таблицы
    columns = ("id", "date")
    tree = ttk.Treeview(day_window, columns=columns, show="headings")

    # Заголовки колонок
    for col in columns:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=100, anchor="center")

    tree.pack(fill=tk.BOTH, expand=True)

    # Кнопки
    button_frame = tk.Frame(day_window)
    button_frame.pack(pady=10)

    btn_refresh = tk.Button(button_frame, text="Обновить таблицу", command=lambda: fetch_days(tree))
    btn_refresh.grid(row=0, column=0, padx=10)

    btn_create = tk.Button(button_frame, text="Создать день", command=lambda: create_day(tree))
    btn_create.grid(row=0, column=1, padx=10)

    btn_open_pari = tk.Button(button_frame, text="Открыть пары", command=lambda: to_pari(tree, day_window))
    btn_open_pari.grid(row=0, column=2, padx=10)

    btn_back_to_main = tk.Button(button_frame, text="К главному экрану", command=lambda: to_main(day_window))
    btn_back_to_main.grid(row=0, column=3, padx=10)

    # Загружаем дни
    fetch_days(tree)

    day_window.mainloop()

def open_teacher_window():
    # Создаем новое окно учителей поверх основного окна
    teacher_window = tk.Toplevel(window)
    teacher_window.title("Учителя")
    teacher_window.geometry("800x400")

    # Заголовок
    label = tk.Label(teacher_window, text="Список учителей", font=("Arial", 14))
    label.pack(pady=10)

    # Создание таблицы
    columns = ("id", "name", "fullname", "login", "gmail", "vk")
    tree = ttk.Treeview(teacher_window, columns=columns, show="headings")

    # Заголовки колонок
    for col in columns:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=100, anchor="center")

    tree.pack(fill=tk.BOTH, expand=True)

    # Кнопки
    button_frame = tk.Frame(teacher_window)
    button_frame.pack(pady=10)

    btn_refresh = tk.Button(button_frame, text="Обновить таблицу", command=lambda: fetch_teachers(tree))
    btn_refresh.grid(row=0, column=0, padx=10)

    btn_create = tk.Button(button_frame, text="Создать учителя", command=lambda: create_teacher(tree))
    btn_create.grid(row=0, column=1, padx=10)

    btn_edit = tk.Button(button_frame, text="Редактировать учителя", command=lambda: edit_teacher(tree))
    btn_edit.grid(row=0, column=2, padx=10)

    btn_delete = tk.Button(button_frame, text="Удалить учителя", command=lambda: delete_teacher(tree))
    btn_delete.grid(row=0, column=3, padx=10)

    btn_back_to_main = tk.Button(button_frame, text="К главному экрану", command=lambda: to_main(teacher_window))
    btn_back_to_main.grid(row=0, column=4, padx=10)

    # Загружаем учителей
    fetch_teachers(tree)

    teacher_window.mainloop()

def open_student_window():
    # Создаем новое окно студентов поверх основного окна
    student_window = tk.Toplevel(window)
    student_window.title("Студенты")
    student_window.geometry("800x400")

    # Заголовок
    label = tk.Label(student_window, text="Список студентов", font=("Arial", 14))
    label.pack(pady=10)

    # Создание таблицы
    columns = ("id", "name", "fullname", "login", "gmail", "group", "srbal", "vk")
    tree = ttk.Treeview(student_window, columns=columns, show="headings")

    # Заголовки колонок
    for col in columns:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=100, anchor="center")

    tree.pack(fill=tk.BOTH, expand=True)

    # Кнопки
    button_frame = tk.Frame(student_window)
    button_frame.pack(pady=10)

    btn_refresh = tk.Button(button_frame, text="Обновить таблицу", command=lambda: fetch_students(tree))
    btn_refresh.grid(row=0, column=0, padx=10)

    btn_create = tk.Button(button_frame, text="Создать студента", command=lambda: create_student(tree))
    btn_create.grid(row=0, column=1, padx=10)

    btn_edit = tk.Button(button_frame, text="Редактировать студента", command=lambda: edit_student(tree))
    btn_edit.grid(row=0, column=2, padx=10)

    btn_delete = tk.Button(button_frame, text="Удалить студента", command=lambda: delete_student(tree))
    btn_delete.grid(row=0, column=3, padx=10)

    btn_back_to_main = tk.Button(button_frame, text="К главному экрану", command=lambda: to_main(student_window))
    btn_back_to_main.grid(row=0, column=4, padx=10)

    # Загружаем студентов
    fetch_students(tree)

    student_window.mainloop()


def open_main_window():
    global window
    window = tk.Tk()
    window.title("Админ панель kkts")
    window.geometry("400x300")

    btn_student = tk.Button(window, text="Перейти к студентам", command=to_student)
    btn_student.grid(row=0, column=2, padx=10)

    btn_teacher = tk.Button(window, text="Перейти к учителям", command=to_teacher)
    btn_teacher.grid(row=1, column=2, padx=20)
    btn_teacher = tk.Button(window, text="Перейти к дням", command=to_day)
    btn_teacher.grid(row=2, column=2, padx=20)

    window.mainloop()


open_main_window()
