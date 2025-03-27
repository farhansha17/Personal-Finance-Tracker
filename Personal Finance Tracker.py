import sqlite3
import tkinter as tk
from tkinter import messagebox

# Database setup
def setup_db():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            category TEXT, 
            amount REAL,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()

# Function to add transactions
def add_transaction(type, category, amount):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (type, category, amount, date) VALUES (?, ?, ?, date('now'))", 
                   (type, category, amount))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Transaction Added!")
    update_balance()

# Function to get total balance
def get_balance():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='Income'")
    income = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='Expense'")
    expense = cursor.fetchone()[0] or 0
    conn.close()
    return income - expense

# Function to update balance label
def update_balance():
    balance = get_balance()
    balance_label.config(text=f"Balance: ${balance:.2f}")

# GUI Setup
setup_db()
root = tk.Tk()
root.title("Personal Finance Tracker")
root.geometry("300x250")

# UI Elements
tk.Label(root, text="Transaction Type").pack()
type_var = tk.StringVar()
type_var.set("Income")
tk.OptionMenu(root, type_var, "Income", "Expense").pack()

tk.Label(root, text="Category").pack()
category_entry = tk.Entry(root)
category_entry.pack()

tk.Label(root, text="Amount").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

tk.Button(root, text="Add Transaction", command=lambda: add_transaction(
    type_var.get(), category_entry.get(), float(amount_entry.get()))).pack()

balance_label = tk.Label(root, text=f"Balance: ${get_balance():.2f}", font=("Arial", 12, "bold"))
balance_label.pack()

update_balance()
root.mainloop()
