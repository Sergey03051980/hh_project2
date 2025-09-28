import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from .config import DEFAULT_DB_CONFIG, WORK_DB_CONFIG, DB_NAME  # Изменено!


class DatabaseManager:
    """Класс для управления созданием БД и таблиц"""

    def __init__(self):
        self.default_config = DEFAULT_DB_CONFIG
        self.work_config = WORK_DB_CONFIG
        self.db_name = DB_NAME

    def create_database(self):
        """Создание новой базы данных"""
        try:
            # Подключаемся к БД postgres для создания новой БД
            conn = psycopg2.connect(**self.default_config)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

            with conn.cursor() as cur:
                # Проверяем, существует ли БД
                cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (self.db_name,))
                exists = cur.fetchone()

                if not exists:
                    # Создаем новую БД
                    create_db_query = sql.SQL("CREATE DATABASE {}").format(
                        sql.Identifier(self.db_name)
                    )
                    cur.execute(create_db_query)
                    print(f"✅ База данных '{self.db_name}' создана успешно")
                    result = True
                else:
                    print(f"✅ База данных '{self.db_name}' уже существует")
                    result = True

            conn.close()
            return result

        except Exception as error:
            print(f"❌ Ошибка при создании БД: {error}")
            return False

    def create_connection(self, use_work_db=True):
        """Создание подключения к БД"""
        config = self.work_config if use_work_db else self.default_config
        return psycopg2.connect(**config)

    def create_tables(self):
        """Создание таблиц в рабочей БД"""
        commands = (
            """
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                url VARCHAR(500)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS vacancies (
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
        )

        conn = None
        try:
            conn = self.create_connection()
            cur = conn.cursor()

            for command in commands:
                cur.execute(command)

            cur.close()
            conn.commit()
            print("✅ Таблицы созданы успешно")
            return True

        except Exception as error:
            print(f"❌ Ошибка при создании таблиц: {error}")
            return False
        finally:
            if conn is not None:
                conn.close()

    def check_database_exists(self):
        """Упрощенная проверка существования БД"""
        try:
            conn = self.create_connection()
            if conn:
                conn.close()
                return True
            return False
        except:
            return False

    def setup_database(self):
        """Полная настройка БД: создание БД + таблиц"""
        print("🔄 Настройка базы данных...")

        try:
            # 1. Создаем БД (если не существует)
            print("📦 Шаг 1: Проверка/создание БД...")
            if not self.create_database():
                return False

            # 2. Задержка для гарантии создания БД
            import time
            time.sleep(2)

            # 3. Создаем таблицы
            print("📦 Шаг 2: Создание таблиц...")
            if not self.create_tables():
                return False

            # 4. Простая проверка - пытаемся подключиться
            print("📦 Шаг 3: Проверка доступности...")
            conn = self.create_connection()
            if conn:
                conn.close()
                print("✅ База данных настроена успешно")
                return True
            else:
                print("❌ Не удалось подключиться к БД после настройки")
                return False

        except Exception as error:
            print(f"❌ Ошибка при настройке базы данных: {error}")
            return False


    def insert_company(self, company):
        """Добавление компании в БД"""
        conn = self.create_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO companies (id, name, description, url)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                    name = EXCLUDED.name,
                    description = EXCLUDED.description,
                    url = EXCLUDED.url
                """, (company.id, company.name, company.description, company.url))
            conn.commit()
        except Exception as e:
            print(f"Ошибка при добавлении компании {company.name}: {e}")
        finally:
            conn.close()

    def insert_vacancy(self, vacancy):
        """Добавление вакансии в БД"""
        conn = self.create_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO vacancies (id, name, company_id, salary_from, 
                                         salary_to, currency, url, description)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                    name = EXCLUDED.name,
                    salary_from = EXCLUDED.salary_from,
                    salary_to = EXCLUDED.salary_to,
                    currency = EXCLUDED.currency,
                    url = EXCLUDED.url,
                    description = EXCLUDED.description
                """, (vacancy.id, vacancy.name, vacancy.company_id,
                      vacancy.salary_from, vacancy.salary_to, vacancy.currency,
                      vacancy.url, vacancy.description))
            conn.commit()
        except Exception as e:
            print(f"Ошибка при добавлении вакансии {vacancy.name}: {e}")
        finally:
            conn.close()
