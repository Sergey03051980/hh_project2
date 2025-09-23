from hh_project2.database import DatabaseManager
from hh_project2.api import HHAPI
from hh_project2.config import COMPANIES


def test_integration_flow():
    """Интеграционный тест полного потока данных"""
    print("🚀 Запуск интеграционного теста...")

    # Инициализация
    db = DatabaseManager()
    api = HHAPI()

    # Создание таблиц
    db.create_tables()
    print("✅ Таблицы созданы")

    # Тест одной компании
    company_info = COMPANIES[0]  # Яндекс
    print(f"🔄 Тестируем компанию: {company_info['name']}")

    company = api.parse_company_data(company_info['id'], company_info['name'])

    # Сохранение компании
    db.insert_company(company)
    print(f"✅ Компания {company.name} сохранена")

    # Получение вакансий (ограничим количество для теста)
    vacancies_data = api.get_vacancies_by_employer(company_info['id'])
    print(f"✅ Получено вакансий: {len(vacancies_data)}")

    # Сохранение нескольких вакансий
    saved_count = 0
    for vacancy_data in vacancies_data[:3]:  # Сохраним только 3 для теста
        vacancy = api.parse_vacancy_data(vacancy_data)
        db.insert_vacancy(vacancy)
        saved_count += 1

    print(f"✅ Сохранено вакансий: {saved_count}")
    print("✅ Интеграционный тест завершен успешно")


if __name__ == "__main__":
    test_integration_flow()
