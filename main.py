import tkinter as tk
from tkinter import messagebox, ttk
import json
import random
import os

# --- Конфигурация ---
HISTORY_FILE = "tasks.json"

# Предопределённые задачи
DEFAULT_TASKS = [
    {"name": "Прочитать статью", "type": "учёба"},
    {"name": "Сделать зарядку", "type": "спорт"},
    {"name": "Написать отчёт", "type": "работа"},
    {"name": "Посмотреть обучающее видео", "type": "учёба"},
    {"name": "Погулять на свежем воздухе", "type": "спорт"},
    {"name": "Провести рабочее совещание", "type": "работа"},
]

# --- Глобальные переменные ---
all_tasks = DEFAULT_TASKS.copy()  # Основной список задач (можно пополнять)
history = []  # История сгенерированных задач

# --- Функции работы с файлом ---
def load_history():
    """Загружает историю из JSON-файла."""
    global history
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except (json.JSONDecodeError, Exception):
            history = []
    else:
        history = []

def save_history():
    """Сохраняет историю в JSON-файл."""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

# --- Функции логики приложения ---
def generate_task():
    """Генерирует случайную задачу и добавляет её в историю."""
    task = random.choice(all_tasks)
    history.append(task)
    update_history_display()
    save_history()

def update_history_display(*args):
    """Обновляет видимый список задач в зависимости от фильтра."""
    selected_type = filter_var.get()
    filtered_history = history if selected_type == "все" else [t for t in history if t["type"] == selected_type]
    
    listbox_history.delete(0, tk.END)
    for task in filtered_history:
        listbox_history.insert(tk.END, f"{task['name']} ({task['type']})")

def add_new_task():
    """Добавляет новую задачу в список после проверки."""
    name = entry_task_name.get().strip()
    task_type = combo_task_type.get()

    if not name:
        messagebox.showerror("Ошибка", "Название задачи не может быть пустым!")
        return

    new_task = {"name": name, "type": task_type}
    all_tasks.append(new_task)

    # Очистка полей
    entry_task_name.delete(0, tk.END)
    combo_task_type.set("учёба")

    messagebox.showinfo("Успех", f"Задача '{name}' добавлена в список!")

# --- Инициализация GUI ---
root = tk.Tk()
root.title("Random Task Generator")
root.geometry("500x500")
root.resizable(False, False)

# --- Вкладка Генерации ---
frame_generate = tk.LabelFrame(root, text="Генерация задачи", padx=10, pady=10)
frame_generate.pack(padx=10, pady=10, fill="x")

btn_generate = tk.Button(frame_generate, text="Сгенерировать задачу", font=("Arial", 12), command=generate_task)
btn_generate.pack(pady=5)

# --- Вкладка Истории ---
frame_history = tk.LabelFrame(root, text="История задач", padx=10, pady=10)
frame_history.pack(padx=10, pady=10, fill="both", expand=True)

filter_var = tk.StringVar(value="все")
filter_var.trace_add("write", update_history_display) # Отслеживаем изменения фильтра

label_filter = tk.Label(frame_history, text="Фильтр по типу:")
label_filter.pack(anchor="w")

combo_filter = ttk.Combobox(frame_history, textvariable=filter_var,
                            values=["все", "учёба", "спорт", "работа"], state="readonly")
combo_filter.pack(pady=5, anchor="w")

scrollbar = tk.Scrollbar(frame_history)
scrollbar.pack(side="right", fill="y")

listbox_history = tk.Listbox(frame_history, yscrollcommand=scrollbar.set, width=60, height=15)
listbox_history.pack(padx=5, pady=5, fill="both", expand=True)
scrollbar.config(command=listbox_history.yview)

# --- Вкладка Добавления новой задачи ---
frame_add = tk.LabelFrame(root, text="Добавить свою задачу", padx=10, pady=10)
frame_add.pack(padx=10, pady=10, fill="x")

label_name = tk.Label(frame_add, text="Название задачи:")
label_name.grid(row=0, column=0, sticky="e", padx=5, pady=2)

entry_task_name = tk.Entry(frame_add, width=40)
entry_task_name.grid(row=0, column=1, columnspan=2, sticky="w", padx=5, pady=2)

label_type = tk.Label(frame_add, text="Тип задачи:")
label_type.grid(row=1, column=0, sticky="e", padx=5, pady=2)

combo_task_type = ttk.Combobox(frame_add, values=["учёба", "спорт", "работа"], state="readonly")
combo_task_type.grid(row=1, column=1, sticky="w", padx=5, pady=2)
combo_task_type.set("учёба")

btn_add = tk.Button(frame_add, text="Добавить задачу", command=add_new_task)
btn_add.grid(row=2, column=1, sticky="e", padx=5, pady=10)

# --- Запуск приложения ---
if __name__ == "__main__":
    load_history()  # Загружаем историю при старте
    update_history_display()  # Обновляем отображение истории
    root.mainloop()