import tkinter as tk
from tkinter import ttk, messagebox
import database as db

class ColdStorageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Учет продукции - АО 'Курский хладокомбинат'")
        self.root.geometry("850x550")
        
        db.init_db()
        
        manage_frame = tk.LabelFrame(self.root, text="Управление данными товара", font=("Arial", 10, "bold"))
        manage_frame.pack(fill="x", padx=15, pady=10)
        
        tk.Label(manage_frame, text="Наименование:").grid(row=0, column=0, padx=5, pady=10, sticky="e")
        self.entry_name = tk.Entry(manage_frame, width=20)
        self.entry_name.grid(row=0, column=1, padx=5, pady=10)
        
        tk.Label(manage_frame, text="Категория:").grid(row=0, column=2, padx=5, pady=10, sticky="e")
        self.combo_category = ttk.Combobox(manage_frame, values=["Мороженое", "Десерт", "Фруктовый лед"], width=15)
        self.combo_category.grid(row=0, column=3, padx=5, pady=10)
        self.combo_category.current(0)
        
        tk.Label(manage_frame, text="Кол-во (шт):").grid(row=0, column=4, padx=5, pady=10, sticky="e")
        self.entry_qty = tk.Entry(manage_frame, width=10)
        self.entry_qty.grid(row=0, column=5, padx=5, pady=10)
        
        tk.Label(manage_frame, text="Дата партии:").grid(row=0, column=6, padx=5, pady=10, sticky="e")
        self.entry_date = tk.Entry(manage_frame, width=12)
        self.entry_date.insert(0, "2026-02-24")  # Значение по умолчанию со скриншота
        self.entry_date.grid(row=0, column=7, padx=5, pady=10)
        
        btn_add = tk.Button(manage_frame, text="Добавить новый", bg="#4CAF50", fg="white", command=self.handle_add_product)
        btn_add.grid(row=0, column=8, padx=10, pady=10)
        
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=15, pady=5)
        
        columns = ("id", "name", "category", "qty", "date")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Наименование товара")
        self.tree.heading("category", text="Категория")
        self.tree.heading("qty", text="Количество (шт)")
        self.tree.heading("date", text="Дата производства")
        
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("name", width=250, anchor="w")
        self.tree.column("category", width=150, anchor="center")
        self.tree.column("qty", width=100, anchor="center")
        self.tree.column("date", width=150, anchor="center")
        
        self.tree.pack(fill="both", expand=True)
        
        # Нижняя кнопка удаления
        btn_delete = tk.Button(self.root, text="Удалить выбранную позицию", bg="#D32F2F", fg="white", command=self.handle_delete_product)
        btn_delete.pack(anchor="w", padx=15, pady=10)
        
        # Загрузка первичных данных в таблицу
        self.load_table_data()

    def load_table_data(self):
        """Очищает интерфейсную таблицу и загружает актуальные данные из SQLite."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        products = db.fetch_all_products()
        for prod in products:
            self.tree.insert("", "end", values=prod)

    def handle_add_product(self):
        """Обработчик события добавления элемента с валидацией входных данных."""
        name = self.entry_name.get().strip()
        category = self.combo_category.get()
        qty_str = self.entry_qty.get().strip()
        date = self.entry_date.get().strip()
        
        if not name or not qty_str or not date:
            messagebox.showwarning("Ошибка ввода", "Пожалуйста, заполните все текстовые поля!")
            return
            
        try:
            quantity = int(qty_str)
        except ValueError:
            messagebox.showerror("Ошибка типа", "Поле 'Количество' должно содержать только целые числа!")
            return
            
        db.add_new_product(name, category, quantity, date)
        self.load_table_data()
        
        # Очистка полей после успешной отправки
        self.entry_name.delete(0, tk.END)
        self.entry_qty.delete(0, tk.END)

    def handle_delete_product(self):
        """Удаляет выделенную в Treeview строку из базы данных."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Выделение отсутствует", "Выберите строку в таблице для удаления!")
            return
            
        item_values = self.tree.item(selected_item, "values")
        product_id = item_values[0]
        
        db.delete_product_by_id(product_id)
        self.load_table_data()

if __name__ == "__main__":
    root = tk.Tk()
    app = ColdStorageApp(root)
    root.mainloop()