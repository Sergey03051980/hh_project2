# hh_project2/api/hh_api.py
import requests
from typing import List, Dict, Optional
import time


class HeadHunterAPI:
    """Класс для работы с API HeadHunter"""

    def __init__(self):
        self.base_url = "https://api.hh.ru"
        self.headers = {
            "User-Agent": "HH-API-Project/1.0 (serzh466163@gmail.com)",
            "Accept": "application/json"
        }
        self.delay = 0.2

    def _make_request(self, url: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Универсальный метод для выполнения запросов"""
        try:
            time.sleep(self.delay)
            response = requests.get(url, headers=self.headers, params=params, timeout=10)

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Ошибка {response.status_code} для URL: {url}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса к {url}: {e}")
            return None

    def get_employer(self, employer_id: int) -> Optional[Dict]:
        """Получает информацию о работодателе"""
        url = f"{self.base_url}/employers/{employer_id}"
        return self._make_request(url)

    def get_vacancies(self, employer_id: int, page: int = 0, per_page: int = 50) -> List[Dict]:
        """
        Получает вакансии работодателя

        Args:
            employer_id: ID работодателя
            page: Номер страницы
            per_page: Количество вакансий на странице

        Returns:
            List[Dict]: Список вакансий
        """
        url = f"{self.base_url}/vacancies"
        params = {
            "employer_id": employer_id,
            "page": page,
            "per_page": per_page
        }

        data = self._make_request(url, params)
        return data.get("items", []) if data else []

    def get_all_vacancies(self, employer_id: int, max_pages: int = 5) -> List[Dict]:
        """
        Получает все вакансии работодателя (с пагинацией)

        Args:
            employer_id: ID работодателя
            max_pages: Максимальное количество страниц для парсинга

        Returns:
            List[Dict]: Все вакансии работодателя
        """
        all_vacancies = []

        for page in range(max_pages):
            vacancies = self.get_vacancies(employer_id, page=page)
            if not vacancies:
                break
            all_vacancies.extend(vacancies)
            print(f"Страница {page + 1}: получено {len(vacancies)} вакансий")

        return all_vacancies


# Для тестирования
if __name__ == "__main__":
    api = HeadHunterAPI()

    # Тест работодателя
    employer = api.get_employer(1455)
    if employer:
        print(f"✅ Работодатель: {employer.get('name')}")

    # Тест вакансий
    vacancies = api.get_all_vacancies(1455, max_pages=2)
    print(f"✅ Всего получено вакансий: {len(vacancies)}")

    if vacancies:
        for i, vacancy in enumerate(vacancies[:3]):
            print(f"{i + 1}. {vacancy.get('name')}")


def get_vacancies(self, employer_id: int, page: int = 0, per_page: int = 50) -> List[Dict]:
    """
    Получает вакансии работодателя
    """
    url = f"{self.base_url}/vacancies"
    params = {
        "employer_id": employer_id,
        "page": page,
        "per_page": per_page,
        "only_with_salary": False  # Получаем все вакансии, даже без зарплаты
    }

    data = self._make_request(url, params)
    if data and 'items' in data:
        return data['items']
    return []


def print_vacancy_info(self, vacancy: Dict) -> None:
    """Печатает информацию о вакансии в читаемом формате"""
    salary = vacancy.get('salary')
    if salary:
        salary_from = salary.get('from', '?')
        salary_to = salary.get('to', '?')
        currency = salary.get('currency', '')
        salary_info = f"{salary_from}-{salary_to} {currency}"
    else:
        salary_info = "не указана"

    print(f"💼 {vacancy.get('name')}")
    print(f"   Зарплата: {salary_info}")
    print(f"   URL: {vacancy.get('alternate_url')}")
    print(f"   Работодатель: {vacancy.get('employer', {}).get('name', 'не указан')}")
    print()
