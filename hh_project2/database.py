import psycopg2
from .config import DB_CONFIG  # Изменено здесь!


class DatabaseManager:
    """Класс для управления базой данных"""

    def __init__(self):
        self.config = DB_CONFIG

    def create_connection(self):
        """Создание подключения к БД"""
        return psycopg2.connect(**self.config)

    def create_tables(self):
        """Создание таблиц в базе данных"""
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

        except Exception as error:
            print(f"❌ Ошибка при создании таблиц: {error}")
        finally:
            if conn is not None:
                conn.close()

    def insert_company(self, company) -> None:
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

    def insert_vacancy(self, vacancy) -> None:
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
