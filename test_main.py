import pytest
import os
import database as db

@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Фикстура для изоляции тестов и работы с чистой временной БД."""
    db.DB_NAME = "test_cold_storage.db"
    db.init_db()
    yield
    if os.path.exists("test_cold_storage.db"):
        os.remove("test_cold_storage.db")

def test_db_initialization():
    """Тест 1: Проверка создания файла БД и корректности инициализации пустого хранилища."""
    products = db.fetch_all_products()
    assert isinstance(products, list)
    assert len(products) == 0

def test_add_product():
    """Тест 2: Проверка успешной вставки строки в таблицу и чтения сохраненных значений."""
    db.add_new_product("Пломбир Ванильный", "Мороженое", 300, "2026-02-24")
    products = db.fetch_all_products()
    assert len(products) == 1
    assert products[0][1] == "Пломбир Ванильный"
    assert products[0][3] == 300

def test_delete_product():
    """Тест 3: Проверка корректного удаления добавленного объекта по его первичному ключу ID."""
    db.add_new_product("Эскимо в глазури", "Мороженое", 150, "2026-02-23")
    products_before = db.fetch_all_products()
    prod_id = products_before[0][0]
    
    db.delete_product_by_id(prod_id)
    products_after = db.fetch_all_products()
    assert len(products_after) == 0