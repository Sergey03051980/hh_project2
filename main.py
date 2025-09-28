from hh_project2.database_manager import DatabaseManager
from hh_project2.api import HHAPI
from hh_project2.db_manager import DBManager
from hh_project2.config import COMPANIES
import time
import sys


def setup_database():
    """Настройка базы данных: создание БД и таблиц"""
    db_manager = DatabaseManager()

    print("🔍 Проверяем существование БД...")

    # Простая проверка: пытаемся подключиться к рабочей БД
    try:
        conn = db_manager.create_connection(use_work_db=True)
        if conn:
            conn.close()
            print("✅ База данных уже существует и доступна")
            return True
    except:
        print("❌ Не удалось подключиться к БД")

    # Если не удалось подключиться, создаем БД
    print("🔄 Создаем новую базу данных...")
    return db_manager.setup_database()


def load_data_to_db():
    """Загрузка данных из API в базу данных"""
    hh_api = HHAPI()
    db_manager = DatabaseManager()

    # Сначала проверим, есть ли уже данные
    try:
        test_conn = db_manager.create_connection()
        test_cur = test_conn.cursor()
        test_cur.execute("SELECT COUNT(*) FROM companies")
        companies_count = test_cur.fetchone()[0]
        test_cur.execute("SELECT COUNT(*) FROM vacancies")
        vacancies_count = test_cur.fetchone()[0]
        test_cur.close()
        test_conn.close()

        if companies_count > 0 and vacancies_count > 0:
            print(f"✅ В БД уже есть данные: {companies_count} компаний, {vacancies_count} вакансий")
            print("🔄 Пропускаем загрузку данных...")
            return True
    except:
        pass  # Если ошибка - продолжаем загрузку

    print("📥 Загрузка данных с hh.ru...")

    total_vacancies = 0
    successful_companies = 0

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
            successful_companies += 1
            print(f"✅ {company_info['name']}: загружено {vacancy_count} вакансий")
            time.sleep(0.5)

        except Exception as e:
            print(f"❌ Ошибка при обработке {company_info['name']}: {e}")

    print(f"📊 Итоги загрузки: {successful_companies}/{len(COMPANIES)} компаний, {total_vacancies} вакансий")
    return successful_companies > 0


def user_interface():
    """Пользовательский интерфейс"""
    try:
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
            print("6. 📊 Статистика")
            print("0. ❌ Выход")
            print("=" * 50)

            choice = input("Выберите действие: ").strip()

            if choice == "1":
                print("\n📈 Компании и количество вакансий:")
                print("-" * 50)
                results = db_manager.get_companies_and_vacancies_count()
                if results:
                    for i, (company, count) in enumerate(results, 1):
                        print(f"{i:2d}. {company:<20} | {count:>4} вакансий")
                else:
                    print("❌ Нет данных о компаниях")

            elif choice == "2":
                print("\n💼 Все вакансии (первые 20):")
                print("-" * 80)
                results = db_manager.get_all_vacancies()
                if results:
                    for i, (company, vacancy, salary_from, salary_to, currency, url) in enumerate(results[:20], 1):
                        if salary_from or salary_to:
                            salary_str = f"{salary_from or '?'}-{salary_to or '?'} {currency}"
                        else:
                            salary_str = "не указана"
                        print(f"{i:2d}. {company:<15} | {vacancy:<30} | {salary_str}")
                else:
                    print("❌ Нет данных о вакансиях")

            elif choice == "3":
                print("\n💰 Средняя зарплата:")
                print("-" * 30)
                avg_salary = db_manager.get_avg_salary()
                print(f"Средняя зарплата: {avg_salary:,.2f} руб.")

            elif choice == "4":
                print("\n🚀 Вакансии с зарплатой выше средней (первые 20):")
                print("-" * 80)
                results = db_manager.get_vacancies_with_higher_salary()
                if results:
                    avg_salary = db_manager.get_avg_salary()
                    print(f"Средняя зарплата: {avg_salary:,.2f} руб.")
                    print("-" * 80)

                    for i, (company, vacancy, salary_from, salary_to, currency, url) in enumerate(results[:20], 1):
                        if salary_from or salary_to:
                            avg_vacancy = (salary_from or 0 + salary_to or 0) / 2
                            salary_str = f"{salary_from or '?'}-{salary_to or '?'} {currency} (avg: {avg_vacancy:,.0f})"
                        else:
                            salary_str = "не указана"
                        print(f"{i:2d}. {company:<15} | {vacancy:<30} | {salary_str}")
                else:
                    print("❌ Нет вакансий с зарплатой выше средней")

            elif choice == "5":
                keyword = input("\n🔍 Введите ключевое слово для поиска: ").strip()
                if keyword:
                    print(f"\nРезультаты поиска по '{keyword}':")
                    print("-" * 80)
                    results = db_manager.get_vacancies_with_keyword(keyword)
                    if results:
                        for i, (company, vacancy, salary_from, salary_to, currency, url) in enumerate(results[:20], 1):
                            if salary_from or salary_to:
                                salary_str = f"{salary_from or '?'}-{salary_to or '?'} {currency}"
                            else:
                                salary_str = "не указана"
                            print(f"{i:2d}. {company:<15} | {vacancy:<30} | {salary_str}")
                    else:
                        print("❌ Вакансий по вашему запросу не найдено")
                else:
                    print("❌ Введите ключевое слово")

            elif choice == "6":
                print("\n📊 Статистика:")
                print("-" * 30)
                # Общая статистика
                companies = db_manager.get_companies_and_vacancies_count()
                vacancies = db_manager.get_all_vacancies()
                avg_salary = db_manager.get_avg_salary()
                high_salary = db_manager.get_vacancies_with_higher_salary()

                print(f"Количество компаний: {len(companies)}")
                print(f"Общее количество вакансий: {len(vacancies)}")
                print(f"Средняя зарплата: {avg_salary:,.2f} руб.")
                print(f"Вакансий с зарплатой выше средней: {len(high_salary)}")

            elif choice == "0":
                print("\n👋 До свидания!")
                break
            else:
                print("❌ Неверный выбор. Попробуйте снова.")

            # Пауза после вывода результатов
            if choice in ['1', '2', '3', '4', '5', '6']:
                input("\n↵ Нажмите Enter для продолжения...")

    except Exception as e:
        print(f"❌ Ошибка в пользовательском интерфейсе: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Основная функция"""
    print("🚀 Запуск HH Project 2.0!")

    try:
        # Настройка БД: создание БД и таблиц
        if not setup_database():
            print("❌ Не удалось настроить базу данных. Программа завершена.")
            return

        # Загрузка данных
        if not load_data_to_db():
            print("⚠️ Данные не загружены, но можно использовать существующие")

        # Запуск интерфейса
        user_interface()

    except KeyboardInterrupt:
        print("\n👋 Программа завершена пользователем")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
