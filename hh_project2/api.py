import requests
import time
from typing import List, Dict, Any
from .models import Company, Vacancy  # Изменено здесь!
from .config import HH_API_URL  # И здесь!


class HHAPI:
    """Класс для работы с API HeadHunter"""

    def __init__(self):
        self.base_url = HH_API_URL
        self.headers = {'User-Agent': 'HH-API-App/1.0'}

    def get_employer_info(self, employer_id: int) -> Dict[str, Any]:
        """Получение информации о компании по ID"""
        url = f"{self.base_url}employers/{employer_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_vacancies_by_employer(self, employer_id: int) -> List[Dict[str, Any]]:
        """Получение вакансий компании"""
        url = f"{self.base_url}vacancies"
        params = {
            'employer_id': employer_id,
            'per_page': 100,
            'page': 0
        }

        vacancies = []
        while True:
            try:
                response = requests.get(url, params=params, headers=self.headers)
                response.raise_for_status()
                data = response.json()

                vacancies.extend(data.get('items', []))

                # Проверяем, есть ли следующая страница
                if params['page'] >= data.get('pages', 1) - 1:
                    break
                params['page'] += 1

                # Задержка чтобы не перегружать API
                time.sleep(0.1)

            except requests.RequestException as e:
                print(f"Ошибка при получении вакансий: {e}")
                break

        return vacancies

    def parse_company_data(self, employer_id: int, company_name: str) -> Company:
        """Парсинг данных компании"""
        try:
            employer_data = self.get_employer_info(employer_id)

            return Company(
                id=employer_data['id'],
                name=company_name,
                description=self._clean_text(employer_data.get('description', ''))[:500],
                url=employer_data.get('alternate_url')
            )
        except Exception as e:
            print(f"Ошибка при парсинге компании {company_name}: {e}")
            return Company(id=employer_id, name=company_name)

    def parse_vacancy_data(self, vacancy_data: Dict[str, Any]) -> Vacancy:
        """Парсинг данных вакансии"""
        salary = vacancy_data.get('salary')

        return Vacancy(
            id=int(vacancy_data['id']),
            name=vacancy_data['name'],
            company_id=int(vacancy_data['employer']['id']),
            salary_from=salary.get('from') if salary else None,
            salary_to=salary.get('to') if salary else None,
            currency=salary.get('currency') if salary else None,
            url=vacancy_data.get('alternate_url'),
            description=self._clean_text(vacancy_data.get('description', ''))[:1000]
        )

    def _clean_text(self, text: str) -> str:
        """Очистка текста от HTML тегов"""
        import re
        return re.sub('<[^<]+?>', '', text) if text else ""
