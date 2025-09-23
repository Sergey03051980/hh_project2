import pytest
from hh_project2.api import HHAPI
from hh_project2.models import Company, Vacancy


def test_hh_api_initialization():
    """Тест инициализации API"""
    api = HHAPI()
    assert api.base_url == "https://api.hh.ru/"
    assert 'User-Agent' in api.headers


def test_get_employer_info():
    """Тест получения информации о компании"""
    api = HHAPI()
    employer_info = api.get_employer_info(1740)  # Яндекс

    assert employer_info is not None
    assert 'id' in employer_info
    assert 'name' in employer_info


def test_parse_company_data():
    """Тест парсинга данных компании"""
    api = HHAPI()
    company = api.parse_company_data(1740, "Яндекс")

    assert isinstance(company, Company)
    assert company.id == 1740
    assert company.name == "Яндекс"


def test_parse_vacancy_data():
    """Тест парсинга данных вакансии"""
    api = HHAPI()

    # Создаем mock данные вакансии
    mock_vacancy_data = {
        'id': '123456',
        'name': 'Python Developer',
        'employer': {'id': '1740'},
        'salary': {'from': 100000, 'to': 200000, 'currency': 'RUR'},
        'alternate_url': 'http://example.com',
        'description': 'Test description'
    }

    vacancy = api.parse_vacancy_data(mock_vacancy_data)

    assert isinstance(vacancy, Vacancy)
    assert vacancy.id == 123456
    assert vacancy.name == 'Python Developer'


if __name__ == "__main__":
    test_hh_api_initialization()
    test_get_employer_info()
    test_parse_company_data()
    test_parse_vacancy_data()
    print("✅ Все тесты API прошли успешно!")
