import pytest
from hh_project2.database import DatabaseManager
from hh_project2.models import Company, Vacancy


def test_database_connection():
    """Тест подключения к БД"""
    db = DatabaseManager()
    conn = db.create_connection()
    assert conn is not None
    conn.close()
    print("✅ Тест подключения к БД прошел успешно")


def test_create_tables():
    """Тест создания таблиц"""
    db = DatabaseManager()
    db.create_tables()
    print("✅ Тест создания таблиц прошел успешно")


def test_insert_company():
    """Тест добавления компании"""
    db = DatabaseManager()

    company = Company(
        id=999999,
        name="Test Company",
        description="Test Description",
        url="http://test.com"
    )

    db.insert_company(company)
    print("✅ Тест добавления компании прошел успешно")


def test_insert_vacancy():
    """Тест добавления вакансии"""
    db = DatabaseManager()

    vacancy = Vacancy(
        id=888888,
        name="Test Vacancy",
        company_id=999999,
        salary_from=50000,
        salary_to=100000,
        currency="RUR",
        url="http://test.com/vacancy"
    )

    db.insert_vacancy(vacancy)
    print("✅ Тест добавления вакансии прошел успешно")


if __name__ == "__main__":
    test_database_connection()
    test_create_tables()
    test_insert_company()
    test_insert_vacancy()
