# test_db.py
from hh_project2.database.db_creator import create_database, create_tables

def test_db():
    print("Тестирование создания БД...")
    if create_database():
        print("✅ База данных создана/проверена")
        if create_tables():
            print("✅ Таблицы созданы/проверены")
        else:
            print("❌ Ошибка создания таблиц")
    else:
        print("❌ Ошибка создания БД")

if __name__ == "__main__":
    test_db()
