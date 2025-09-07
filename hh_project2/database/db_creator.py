# hh_project2/database/db_creator.py
import psycopg2
from typing import Optional
# Исправляем импорт - используем абсолютный путь
from hh_project2.utils.config import DB_CONFIG


def create_database(db_name: str = "hh_vacancies") -> bool:
    """
    Создает базу данных PostgreSQL
    """
    try:
        # Подключаемся к стандартной БД postgres
        conn = psycopg2.connect(
            database="postgres",
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"]
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Проверяем существует ли БД
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"✅ База данных '{db_name}' создана")
        else:
            print(f"✅ База данных '{db_name}' уже существует")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"❌ Ошибка при создании базы данных: {e}")
        return False


def create_tables(db_name: str = "hh_vacancies") -> bool:
    """
    Создает таблицы в базе данных
    """
    try:
        conn = psycopg2.connect(
            database=db_name,
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"]
        )
        cursor = conn.cursor()

        # Создаем таблицу employers
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employers (
                employer_id INTEGER PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                url VARCHAR(255),
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Создаем таблицу vacancies
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                vacancy_id INTEGER PRIMARY KEY,
                employer_id INTEGER REFERENCES employers(employer_id),
                title VARCHAR(255) NOT NULL,
                salary_from INTEGER,
                salary_to INTEGER,
                currency VARCHAR(10),
                url VARCHAR(255),
                requirement TEXT,
                responsibility TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        cursor.close()
        conn.close()

        print("✅ Таблицы созданы успешно")
        return True

    except Exception as e:
        print(f"❌ Ошибка при создании таблиц: {e}")
        return False


if __name__ == "__main__":
    print("Тестирование создания БД и таблиц...")
    if create_database():
        create_tables()
