#!/usr/bin/env python3
"""Проверка таблиц в БД hh_db"""

import psycopg2
from hh_project2.config import WORK_DB_CONFIG


def check_tables():
    """Проверка существования таблиц"""
    try:
        print("🔍 Проверяем таблицы в БД hh_db...")

        conn = psycopg2.connect(**WORK_DB_CONFIG)
        cur = conn.cursor()

        # Проверяем существование таблиц
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = cur.fetchall()

        print(f"📋 Найдено таблиц: {len(tables)}")
        for table in tables:
            print(f"   - {table[0]}")

        # Если таблиц нет, создадим их
        if len(tables) == 0:
            print("🔄 Таблицы не найдены, создаем...")

            # Создаем таблицы
            commands = [
                """
                CREATE TABLE companies (
                    id INTEGER PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    url VARCHAR(500)
                )
                """,
                """
                CREATE TABLE vacancies (
                    id INTEGER PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
                    salary_from INTEGER,
                    salary_to INTEGER,
                    currency VARCHAR(10),
                    url VARCHAR(500),
                    description TEXT
                )
                """
            ]

            for command in commands:
                cur.execute(command)

            conn.commit()
            print("✅ Таблицы созданы успешно")

            # Проверяем еще раз
            cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            tables = cur.fetchall()
            print(f"📋 Теперь таблиц: {len(tables)}")
            for table in tables:
                print(f"   - {table[0]}")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"❌ Ошибка: {e}")


if __name__ == "__main__":
    check_tables()
