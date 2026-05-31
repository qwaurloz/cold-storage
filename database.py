import sqlite3

DB_NAME = "cold_storage.db"

def create_connection():
    """Создает подключение к базе данных SQLite."""
    return sqlite3.connect(DB_NAME)

def init_db():
    """Инициализирует таблицу продуктов, если она отсутствует."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            prod_date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def fetch_all_products():
    """Возвращает все записи из таблицы продуктов."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category, quantity, prod_date FROM products")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_new_product(name, category, quantity, prod_date):
    """Добавляет новую партию мороженого в базу данных."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO products (name, category, quantity, prod_date)
        VALUES (?, ?, ?, ?)
    ''', (name, category, quantity, prod_date))
    conn.commit()
    conn.close()

def delete_product_by_id(product_id):
    """Удаляет запись из базы данных по её уникальному ID."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()