#!/usr/bin/env python3
"""Диагностика проблем с созданием БД"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def debug_database_creation():
    """Диагностика создания БД"""

    # Параметры подключения
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'database': 'postgres',  # Подключаемся к основной БД
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', ''),
        'port': os.getenv('DB_PORT', '5432')
    }

    target_db = os.getenv('DB_NAME', 'hh_db')

    print("🔍 Диагностика создания БД")
    print(f"🎯 Целевая БД: {target_db}")
    print(f"🔧 Конфиг: {config}")

    try:
        # 1. Подключаемся к postgres
        conn = psycopg2.connect(**config)
        conn.autocommit = True  # Включаем autocommit для создания БД

        cur = conn.cursor()

        # 2. Проверяем существующие БД
        print("\n📊 Существующие базы данных:")
        cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false")
        databases = [db[0] for db in cur.fetchall()]

        for db in sorted(databases):
            if db == target_db:
                print(f"   ✅ {db} (целевая)")
            else:
                print(f"   📁 {db}")

        # 3. Проверяем, существует ли целевая БД
        if target_db in databases:
            print(f"\n✅ База данных '{target_db}' существует")
        else:
            print(f"\n❌ База данных '{target_db}' НЕ существует")

            # 4. Пытаемся создать БД
            print(f"🔄 Пытаемся создать БД '{target_db}'...")
            try:
                cur.execute(f"CREATE DATABASE {target_db}")
                print(f"✅ БД '{target_db}' создана успешно!")
            except Exception as e:
                print(f"❌ Ошибка при создании БД: {e}")

        # 5. Проверяем права доступа
        print(f"\n🔐 Проверка прав доступа к БД '{target_db}':")
        try:
            test_config = config.copy()
            test_config['database'] = target_db
            test_conn = psycopg2.connect(**test_config)
            test_conn.close()
            print("   ✅ Доступ есть")
        except Exception as e:
            print(f"   ❌ Нет доступа: {e}")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")


if __name__ == "__main__":
    debug_database_creation()
