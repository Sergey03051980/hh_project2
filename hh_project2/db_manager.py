import psycopg2
from typing import List
from decimal import Decimal
from .config import WORK_DB_CONFIG


class DBManager:
    """Класс для работы с данными в рабочей БД"""

    def __init__(self):
        self.config = WORK_DB_CONFIG

    def execute_query(self, query: str, params: tuple = None) -> List[tuple]:
        """Выполнение SQL запроса"""
        conn = psycopg2.connect(**self.config)
        try:
            with conn.cursor() as cur:
                cur.execute(query, params)
                result = cur.fetchall()
            return result
        except Exception as e:
            print(f"❌ Ошибка при выполнении запроса: {e}")
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
                   v.salary_from, v.salary_to, v.currency, v.url
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id
            ORDER BY c.name, 
                     CASE WHEN v.salary_from IS NOT NULL OR v.salary_to IS NOT NULL 
                          THEN COALESCE(v.salary_from, 0) + COALESCE(v.salary_to, 0) 
                          ELSE 0 END DESC
        """
        return self.execute_query(query)

    def get_avg_salary(self) -> float:
        """Получает среднюю зарплату по вакансиям"""
        query = """
            SELECT AVG(
                CASE 
                    WHEN salary_from IS NOT NULL AND salary_to IS NOT NULL THEN (salary_from + salary_to) / 2
                    WHEN salary_from IS NOT NULL THEN salary_from
                    WHEN salary_to IS NOT NULL THEN salary_to
                    ELSE NULL
                END
            ) as avg_salary
            FROM vacancies 
            WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL
        """
        result = self.execute_query(query)
        if result and result[0][0] is not None:
            # Конвертируем Decimal в float
            avg_salary = result[0][0]
            if isinstance(avg_salary, Decimal):
                return float(avg_salary)
            return float(avg_salary)
        return 0.0

    def get_vacancies_with_higher_salary(self) -> List[tuple]:
        """Получает вакансии с зарплатой выше средней"""
        avg_salary = self.get_avg_salary()
        query = """
            SELECT c.name, v.name, v.salary_from, v.salary_to, v.currency, v.url
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id
            WHERE (
                CASE 
                    WHEN v.salary_from IS NOT NULL AND v.salary_to IS NOT NULL THEN (v.salary_from + v.salary_to) / 2
                    WHEN v.salary_from IS NOT NULL THEN v.salary_from
                    WHEN v.salary_to IS NOT NULL THEN v.salary_to
                    ELSE 0
                END
            ) > %s
            ORDER BY (
                CASE 
                    WHEN v.salary_from IS NOT NULL AND v.salary_to IS NOT NULL THEN (v.salary_from + v.salary_to) / 2
                    WHEN v.salary_from IS NOT NULL THEN v.salary_from
                    WHEN v.salary_to IS NOT NULL THEN v.salary_to
                    ELSE 0
                END
            ) DESC
        """
        return self.execute_query(query, (avg_salary,))

    def get_vacancies_with_keyword(self, keyword: str) -> List[tuple]:
        """Получает вакансии по ключевому слову"""
        query = """
            SELECT c.name, v.name, v.salary_from, v.salary_to, v.currency, v.url
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id
            WHERE LOWER(v.name) LIKE LOWER(%s)
            ORDER BY c.name, 
                     CASE WHEN v.salary_from IS NOT NULL OR v.salary_to IS NOT NULL 
                          THEN COALESCE(v.salary_from, 0) + COALESCE(v.salary_to, 0) 
                          ELSE 0 END DESC
        """
        return self.execute_query(query, (f'%{keyword}%',))
