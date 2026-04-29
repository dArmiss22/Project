import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

FILE = "expenses.json"

# Загрузка / сохранение JSON
def load():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Проверки ввода
def check_amount(val):
    try:
        v = float(val)
        return v > 0
    except:
        return False

def check_date(val):
    parts = val.split(".")
    if len(parts) != 3:
        return False
    try:
        d, m, y = int(parts[0]), int(parts[1]), int(parts[2])
        return 1 <= d <= 31 and 1 <= m <= 12 and 1000 <= y <= 9999
    except:
        return False

# Основное приложение
expenses = load()

def update_table():
    """Очищает и заново заполняет таблицу с учётом фильтров."""
    for row in table.get_children():
        table.delete(row)

    cat_filter = filter_cat.get()
    date_filter = filter_date.get()

    total = 0
    for e in expenses:
        # Фильтр по категории
        if cat_filter != "Все" and e["cat"] != cat_filter:
            continue
        # Фильтр по дате
        if date_filter and e["date"] != date_filter:
            continue
        # Добавляем строку
        table.insert("", "end", values=(e["amount"], e["cat"], e["date"]))
        total += e["amount"]

    # Обновляем сумму
    sum_label.config(text=f"Сумма: {total:.2f} руб.")

def add():
    """Добавляет расход после проверок."""
    am = entry_am.get()
    cat = entry_cat.get()
    dt = entry_dt.get()

    if not check_amount(am):
        messagebox.showerror("Ошибка", "Сумма — положительное число!")
        return
    if not cat.strip():
        messagebox.showerror("Ошибка", "Введите категорию!")
        return
    if not check_date(dt):
        messagebox.showerror("Ошибка", "Дата в формате ДД.ММ.ГГГГ!")
        return

    expenses.append({"amount": float(am), "cat": cat.strip(), "date": dt})
    save(expenses)

    entry_am.delete(0, tk.END)
    entry_dt.delete(0, tk.END)

    update_table()

def apply_filters():
    update_table()

def reset_filters():
    filter_cat.set("Все")
    filter_date.delete(0, tk.END)
    update_table()

# --- Окно ---
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("600x500")

# Поля ввода (одна строка)
tk.Label(root, text="Сумма").grid(row=0, column=0)
entry_am = tk.Entry(root, width=10)
entry_am.grid(row=0, column=1)

tk.Label(root, text="Категория").grid(row=0, column=2)
entry_cat = tk.Entry(root, width=12)
entry_cat.grid(row=0, column=3)

tk.Label(root, text="Дата (ДД.ММ.ГГГГ)").grid(row=0, column=4)
entry_dt = tk.Entry(root, width=12)
entry_dt.grid(row=0, column=5)

tk.Button(root, text="Добавить", command=add, bg="lightgreen").grid(row=0, column=6, padx=5)

# Фильтры (одна строка)
tk.Label(root, text="Фильтр:").grid(row=1, column=0, pady=10)
filter_cat = ttk.Combobox(root, values=["Все", "Еда", "Транспорт", "Развлечения", "Покупки", "Другое"], width=12)
filter_cat.set("Все")
filter_cat.grid(row=1, column=1)

filter_date = tk.Entry(root, width=12)
filter_date.grid(row=1, column=2)

tk.Button(root, text="Применить", command=apply_filters).grid(row=1, column=3)
tk.Button(root, text="Сброс", command=reset_filters).grid(row=1, column=4)

# Сумма
sum_label = tk.Label(root, text="Сумма: 0.00 руб.", font=("Arial", 11, "bold"))
sum_label.grid(row=2, column=0, columnspan=7, pady=5)

# Таблица
table = ttk.Treeview(root, columns=("am", "cat", "dt"), show="headings")
table.heading("am", text="Сумма")
table.heading("cat", text="Категория")
table.heading("dt", text="Дата")
table.column("am", width=100)
table.column("cat", width=150)
table.column("dt", width=100)
table.grid(row=3, column=0, columnspan=7, padx=10)

# Загружаем данные
update_table()

root.mainloop()