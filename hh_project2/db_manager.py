import psycopg2
from typing import List
from .config import DB_CONFIG  # Изменено здесь!


class DBManager:
    """Класс для работы с данными в БД"""

    def __init__(self):
        self.config = DB_CONFIG

    def execute_query(self, query: str, params: tuple = None) -> List[tuple]:
        """Выполнение SQL запроса"""
        conn = psycopg2.connect(**self.config)
        try:
            with conn.cursor() as cur:
                cur.execute(query, params)
                result = cur.fetchall()
            return result
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return []
        finally:
            conn.close()

    def get_companies_and_vacancies_count(self) -> List[tuple]:
        """Получает список всех компаний и количество вакансий"""
        query = """
            SELECT c.name, COUNT(v.id) as vacancy_count
            FROM companies c
            LEFT JOIN vacancies v ON c.id = v.company_id
            GROUP BY c.id, c.name
            ORDER BY vacancy_count DESC
        """
        return self.execute_query(query)

    def get_all_vacancies(self) -> List[tuple]:
        """Получает список всех вакансий"""
        query = """
            SELECT c.name, v.name, 
                   COALESCE(v.salary_from, 0) as salary_from,
                   COALESCE(v.salary_to, 0) as salary_to,
                   v.currency, v.url
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id
            ORDER BY c.name, (COALESCE(v.salary_from, 0) + COALESCE(v.salary_to, 0)) / 2 DESC
        """
        return self.execute_query(query)

    def get_avg_salary(self) -> float:
        """Получает среднюю зарплату по вакансиям"""
        query = """
            SELECT AVG((COALESCE(salary_from, 0) + COALESCE(salary_to, 0)) / 2) as avg_salary
            FROM vacancies 
            WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL
        """
        result = self.execute_query(query)
        return round(result[0][0] or 0, 2) if result else 0

    def get_vacancies_with_higher_salary(self) -> List[tuple]:
        """Получает вакансии с зарплатой выше средней"""
        avg_salary = self.get_avg_salary()
        query = """
            SELECT c.name, v.name, 
                   COALESCE(v.salary_from, 0) as salary_from,
                   COALESCE(v.salary_to, 0) as salary_to,
                   v.currency, v.url
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id
            WHERE (COALESCE(v.salary_from, 0) + COALESCE(v.salary_to, 0)) / 2 > %s
            ORDER BY (COALESCE(v.salary_from, 0) + COALESCE(v.salary_to, 0)) / 2 DESC
        """
        return self.execute_query(query, (avg_salary,))

    def get_vacancies_with_keyword(self, keyword: str) -> List[tuple]:
        """Получает вакансии по ключевому слову"""
        query = """
            SELECT c.name, v.name, 
                   COALESCE(v.salary_from, 0) as salary_from,
                   COALESCE(v.salary_to, 0) as salary_to,
                   v.currency, v.url
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id
            WHERE LOWER(v.name) LIKE LOWER(%s)
            ORDER BY c.name, (COALESCE(v.salary_from, 0) + COALESCE(v.salary_to, 0)) / 2 DESC
        """
        return self.execute_query(query, (f'%{keyword}%',))
