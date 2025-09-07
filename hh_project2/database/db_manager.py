# hh_project2/database/db_manager.py
import psycopg2
from typing import List, Dict, Optional, Tuple
# Исправляем импорт
from hh_project2.utils.config import DB_CONFIG


class DBManager:
    """Класс для управления базой данных PostgreSQL"""

    def __init__(self, db_name: str = "hh_vacancies"):
        self.db_name = db_name
        self.connection = None

    def connect(self):
        """Устанавливает соединение с базой данных"""
        try:
            self.connection = psycopg2.connect(
                database=self.db_name,
                user=DB_CONFIG["user"],
                password=DB_CONFIG["password"],
                host=DB_CONFIG["host"],
                port=DB_CONFIG["port"]
            )
            return True
        except Exception as e:
            print(f"❌ Ошибка подключения к БД: {e}")
            return False

    def disconnect(self):
        """Закрывает соединение с базой данных"""
        if self.connection:
            self.connection.close()

    def get_companies_and_vacancies_count(self) -> List[Tuple]:
        """Получает список всех компаний и количество вакансий"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    SELECT e.name, COUNT(v.vacancy_id) 
                    FROM employers e 
                    LEFT JOIN vacancies v ON e.employer_id = v.employer_id 
                    GROUP BY e.name
                """)
                return cursor.fetchall()
        except Exception as e:
            print(f"❌ Ошибка при получении данных: {e}")
            return []

    def get_all_vacancies(self) -> List[Tuple]:
        """Получает список всех вакансий"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    SELECT e.name, v.title, v.salary_from, v.salary_to, v.url 
                    FROM vacancies v 
                    JOIN employers e ON v.employer_id = e.employer_id
                """)
                return cursor.fetchall()
        except Exception as e:
            print(f"❌ Ошибка при получении вакансий: {e}")
            return []

    def get_avg_salary(self) -> float:
        """Получает среднюю зарплату по вакансиям"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    SELECT AVG((salary_from + salary_to) / 2) 
                    FROM vacancies 
                    WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL
                """)
                result = cursor.fetchone()
                return result[0] or 0
        except Exception as e:
            print(f"❌ Ошибка при расчете средней зарплаты: {e}")
            return 0

    def get_vacancies_with_higher_salary(self) -> List[Tuple]:
        """Получает вакансии с зарплатой выше средней"""
        avg_salary = self.get_avg_salary()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    SELECT e.name, v.title, v.salary_from, v.salary_to, v.url 
                    FROM vacancies v 
                    JOIN employers e ON v.employer_id = e.employer_id
                    WHERE (v.salary_from + v.salary_to) / 2 > %s
                """, (avg_salary,))
                return cursor.fetchall()
        except Exception as e:
            print(f"❌ Ошибка при получении вакансий: {e}")
            return []

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple]:
        """Ищет вакансии по ключевому слову"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    SELECT e.name, v.title, v.salary_from, v.salary_to, v.url 
                    FROM vacancies v 
                    JOIN employers e ON v.employer_id = e.employer_id
                    WHERE v.title ILIKE %s
                """, (f"%{keyword}%",))
                return cursor.fetchall()
        except Exception as e:
            print(f"❌ Ошибка при поиске вакансий: {e}")
            return []

    def __enter__(self):
        """Поддержка контекстного менеджера"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Поддержка контекстного менеджера"""
        self.disconnect()
