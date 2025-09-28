import pytest
from hh_project2.database_manager import DatabaseManager
from hh_project2.models import Company, Vacancy


def test_database_manager_initialization():
    """Тест инициализации DatabaseManager"""
    db = DatabaseManager()
    assert db.default_config is not None
    assert db.work_config is not None
    assert db.db_name is not None
    print("✅ DatabaseManager инициализирован успешно")


def test_create_connection():
    """Тест создания подключения"""
    db = DatabaseManager()
    conn = db.create_connection(use_work_db=False)  # Подключение к postgres
    assert conn is not None
    conn.close()
    print("✅ Подключение к БД создано успешно")


def test_check_database_exists():
    """Тест проверки существования БД"""
    db = DatabaseManager()
    exists = db.check_database_exists()
    assert isinstance(exists, bool)
    print(f"✅ Проверка существования БД: {exists}")


def test_create_database():
    """Тест создания БД"""
    db = DatabaseManager()
    result = db.create_database()
    assert result is True
    print("✅ Создание БД прошло успешно")


def test_create_tables():
    """Тест создания таблиц"""
    db = DatabaseManager()
    db.create_tables()
    print("✅ Создание таблиц прошло успешно")


def test_insert_company():
    """Тест вставки компании"""
    db = DatabaseManager()

    company = Company(
        id=999999,
        name="Test Company",
        description="Test Description",
        url="http://test.com"
    )

    db.insert_company(company)
    print("✅ Вставка компании прошла успешно")


def test_insert_vacancy():
    """Тест вставки вакансии"""
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
    print("✅ Вставка вакансии прошла успешно")


def test_setup_database():
    """Тест полной настройки БД"""
    db = DatabaseManager()
    result = db.setup_database()
    assert result is True
    print("✅ Полная настройка БД прошла успешно")


if __name__ == "__main__":
    test_database_manager_initialization()
    test_create_connection()
    test_check_database_exists()
    test_create_database()
    test_create_tables()
    test_insert_company()
    test_insert_vacancy()
    test_setup_database()
    print("🎉 Все тесты DatabaseManager прошли успешно!")
