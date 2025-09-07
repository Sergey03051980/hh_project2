# hh_project2/database/data_saver.py
import psycopg2
from typing import List, Dict
from hh_project2.utils.config import DB_CONFIG
from hh_project2.models.employer import Employer
from hh_project2.models.vacancy import Vacancy


class DataSaver:
    """Класс для сохранения данных в PostgreSQL"""

    def __init__(self, db_name: str = "hh_vacancies"):
        self.db_name = db_name

    def save_employer(self, employer: Employer) -> bool:
        """Сохраняет работодателя в БД"""
        try:
            conn = psycopg2.connect(
                database=self.db_name,
                user=DB_CONFIG["user"],
                password=DB_CONFIG["password"],
                host=DB_CONFIG["host"],
                port=DB_CONFIG["port"]
            )
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO employers (employer_id, name, url, description)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (employer_id) DO UPDATE SET
                    name = EXCLUDED.name,
                    url = EXCLUDED.url,
                    description = EXCLUDED.description
            """, (employer.id, employer.name, employer.url, employer.description))

            conn.commit()
            cursor.close()
            conn.close()
            return True

        except Exception as e:
            print(f"❌ Ошибка сохранения работодателя {employer.id}: {e}")
            return False

    def save_vacancy(self, vacancy: Vacancy) -> bool:
        """Сохраняет вакансию в БД"""
        try:
            conn = psycopg2.connect(
                database=self.db_name,
                user=DB_CONFIG["user"],
                password=DB_CONFIG["password"],
                host=DB_CONFIG["host"],
                port=DB_CONFIG["port"]
            )
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO vacancies (vacancy_id, employer_id, title, salary_from, salary_to, currency, url, requirement, responsibility)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (vacancy_id) DO UPDATE SET
                    title = EXCLUDED.title,
                    salary_from = EXCLUDED.salary_from,
                    salary_to = EXCLUDED.salary_to,
                    currency = EXCLUDED.currency,
                    url = EXCLUDED.url,
                    requirement = EXCLUDED.requirement,
                    responsibility = EXCLUDED.responsibility
            """, (
                vacancy.id, vacancy.employer_id, vacancy.title,
                vacancy.salary_from, vacancy.salary_to, vacancy.currency,
                vacancy.url, vacancy.requirement, vacancy.responsibility
            ))

            conn.commit()
            cursor.close()
            conn.close()
            return True

        except Exception as e:
            print(f"❌ Ошибка сохранения вакансии {vacancy.id}: {e}")
            return False

    def save_vacancies_batch(self, vacancies: List[Vacancy]) -> int:
        """Сохраняет несколько вакансий за раз"""
        success_count = 0
        for vacancy in vacancies:
            if self.save_vacancy(vacancy):
                success_count += 1
        return success_count
