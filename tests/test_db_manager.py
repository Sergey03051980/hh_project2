import pytest
from decimal import Decimal
from hh_project2.db_manager import DBManager


def test_db_manager_initialization():
    """Тест инициализации DBManager"""
    db = DBManager()
    assert db.config is not None
    print("✅ Тест инициализации DBManager прошел успешно")


def test_get_companies_and_vacancies_count():
    """Тест получения компаний и количества вакансий"""
    db = DBManager()
    results = db.get_companies_and_vacancies_count()
    assert isinstance(results, list)
    print(f"✅ Найдено компаний: {len(results)}")

    # Выводим результаты для наглядности
    for company, count in results[:5]:  # Первые 5 компаний
        print(f"  {company}: {count} вакансий")


def test_get_all_vacancies():
    """Тест получения всех вакансий"""
    db = DBManager()
    results = db.get_all_vacancies()
    assert isinstance(results, list)
    print(f"✅ Найдено вакансий: {len(results)}")


def test_get_avg_salary():
    """Тест расчета средней зарплаты"""
    db = DBManager()
    avg_salary = db.get_avg_salary()
    # Исправлено: учитываем что PostgreSQL возвращает Decimal
    assert isinstance(avg_salary, (int, float, Decimal))
    print(f"✅ Средняя зарплата: {avg_salary} руб.")


def test_get_vacancies_with_higher_salary():
    """Тест вакансий с зарплатой выше средней"""
    db = DBManager()
    results = db.get_vacancies_with_higher_salary()
    assert isinstance(results, list)
    print(f"✅ Вакансий с зарплатой выше средней: {len(results)}")


def test_get_vacancies_with_keyword():
    """Тест поиска по ключевому слову"""
    db = DBManager()
    results = db.get_vacancies_with_keyword('python')
    assert isinstance(results, list)
    print(f"✅ Найдено вакансий по 'python': {len(results)}")


# Добавим тест для проверки формата вывода
def test_avg_salary_format():
    """Тест что средняя зарплата является числом"""
    db = DBManager()
    avg_salary = db.get_avg_salary()

    # Проверяем что это число (может быть Decimal)
    assert avg_salary is not None
    assert avg_salary > 0  # Зарплата должна быть положительной
    print(f"✅ Средняя зарплата корректна: {avg_salary}")


if __name__ == "__main__":
    test_db_manager_initialization()
    test_get_companies_and_vacancies_count()
    test_get_all_vacancies()
    test_get_avg_salary()
    test_get_vacancies_with_higher_salary()
    test_get_vacancies_with_keyword()
    test_avg_salary_format()
