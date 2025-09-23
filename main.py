from hh_project2.database import DatabaseManager
from hh_project2.api import HHAPI
from hh_project2.db_manager import DBManager
from hh_project2.config import COMPANIES
import time


def setup_database():
    """Настройка базы данных"""
    db_manager = DatabaseManager()
    print("🔄 Создание таблиц...")
    db_manager.create_tables()


def load_data_to_db():
    """Загрузка данных из API в базу данных"""
    hh_api = HHAPI()
    db_manager = DatabaseManager()

    print("📥 Загрузка данных с hh.ru...")

    total_vacancies = 0
    for company_info in COMPANIES:
        try:
            print(f"🔄 Обрабатываем компанию: {company_info['name']}")

            # Получаем данные компании
            company = hh_api.parse_company_data(company_info['id'], company_info['name'])
            db_manager.insert_company(company)

            # Получаем вакансии компании
            vacancies_data = hh_api.get_vacancies_by_employer(company_info['id'])

            for vacancy_data in vacancies_data:
                vacancy = hh_api.parse_vacancy_data(vacancy_data)
                db_manager.insert_vacancy(vacancy)

            vacancy_count = len(vacancies_data)
            total_vacancies += vacancy_count
            print(f"✅ {company_info['name']}: загружено {vacancy_count} вакансий")
            time.sleep(0.5)

        except Exception as e:
            print(f"❌ Ошибка при обработке {company_info['name']}: {e}")

    print(f"📊 Всего загружено вакансий: {total_vacancies}")


def user_interface():
    """Пользовательский интерфейс"""
    db_manager = DBManager()

    while True:
        print("\n" + "=" * 50)
        print("📊 HH Project 2.0 - Анализ вакансий")
        print("=" * 50)
        print("1. 📈 Компании и количество вакансий")
        print("2. 💼 Все вакансии")
        print("3. 💰 Средняя зарплата")
        print("4. 🚀 Вакансии с зарплатой выше средней")
        print("5. 🔍 Поиск вакансий по ключевому слову")
        print("0. ❌ Выход")
        print("=" * 50)

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            print("\n📈 Компании и количество вакансий:")
            results = db_manager.get_companies_and_vacancies_count()
            for company, count in results:
                print(f"  {company}: {count} вакансий")

        elif choice == "2":
            print("\n💼 Все вакансии:")
            results = db_manager.get_all_vacancies()
            for company, vacancy, salary_from, salary_to, currency, url in results:
                salary = f"{salary_from}-{salary_to} {currency}" if salary_from or salary_to else "не указана"
                print(f"  {company}: {vacancy} | Зарплата: {salary}")

        elif choice == "3":
            avg_salary = db_manager.get_avg_salary()
            print(f"\n💰 Средняя зарплата по всем вакансиям: {avg_salary} руб.")

        elif choice == "4":
            print("\n🚀 Вакансии с зарплатой выше средней:")
            results = db_manager.get_vacancies_with_higher_salary()
            if results:
                for company, vacancy, salary_from, salary_to, currency, url in results:
                    salary = f"{salary_from}-{salary_to} {currency}"
                    print(f"  {company}: {vacancy} | Зарплата: {salary}")
            else:
                print("  Вакансий с зарплатой выше средней не найдено")

        elif choice == "5":
            keyword = input("Введите ключевое слово для поиска: ").strip()
            if keyword:
                print(f"\n🔍 Результаты поиска по '{keyword}':")
                results = db_manager.get_vacancies_with_keyword(keyword)
                if results:
                    for company, vacancy, salary_from, salary_to, currency, url in results:
                        salary = f"{salary_from}-{salary_to} {currency}" if salary_from or salary_to else "не указана"
                        print(f"  {company}: {vacancy} | Зарплата: {salary}")
                else:
                    print("  Вакансий по вашему запросу не найдено")
            else:
                print("❌ Введите ключевое слово")

        elif choice == "0":
            print("👋 До свидания!")
            break
        else:
            print("❌ Неверный выбор. Попробуйте снова.")


def main():
    """Основная функция"""
    print("🚀 Запуск HH Project 2.0!")

    try:
        # Настройка БД
        setup_database()

        # Загрузка данных
        load_data_to_db()

        # Запуск интерфейса
        user_interface()

    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")


if __name__ == "__main__":
    main()
