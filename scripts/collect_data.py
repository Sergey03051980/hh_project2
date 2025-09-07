# scripts/collect_data.py
from hh_project2.api.hh_api import HeadHunterAPI
from hh_project2.database.data_saver import DataSaver
from hh_project2.database.db_creator import create_database, create_tables
from hh_project2.models.employer import Employer
from hh_project2.models.vacancy import Vacancy


def main():
    print("🚀 Начинаем сбор данных с hh.ru")

    # Создаем БД и таблицы
    if create_database():
        create_tables()

    api = HeadHunterAPI()
    saver = DataSaver()

    # Список компаний для сбора
    company_ids = [
        1455,  # HeadHunter
        1122462,  # 1C
        2180,  # OZON
        3529,  # VK
        78638,  # Тинькофф
        907345,  # Сбер
        1057,  # Касперский
        2748,  # Ростелеком
        3776,  # МТС
        39305  # Газпром нефть
    ]

    total_vacancies = 0

    for company_id in company_ids:
        print(f"\n📊 Обрабатываем компанию ID: {company_id}")

        # Получаем данные компании
        company_data = api.get_employer(company_id)
        if not company_data:
            print(f"❌ Не удалось получить данные компании {company_id}")
            continue

        # Создаем объект Employer
        employer = Employer(
            id=company_data.get('id'),
            name=company_data.get('name'),
            url=company_data.get('alternate_url'),
            description=company_data.get('description'),
            vacancies_url=company_data.get('vacancies_url')
        )

        # Сохраняем компанию
        if saver.save_employer(employer):
            print(f"✅ Компания сохранена: {employer.name}")
        else:
            print(f"❌ Ошибка сохранения компании: {employer.name}")
            continue

        # Получаем вакансии
        vacancies_data = api.get_all_vacancies(company_id, max_pages=3)
        print(f"   Получено вакансий: {len(vacancies_data)}")

        # Сохраняем вакансии
        saved_count = 0
        for vac_data in vacancies_data:
            vacancy = Vacancy(
                id=vac_data.get('id'),
                employer_id=company_id,
                title=vac_data.get('name'),
                salary_from=vac_data.get('salary', {}).get('from'),
                salary_to=vac_data.get('salary', {}).get('to'),
                currency=vac_data.get('salary', {}).get('currency'),
                url=vac_data.get('alternate_url'),
                requirement=vac_data.get('snippet', {}).get('requirement'),
                responsibility=vac_data.get('snippet', {}).get('responsibility')
            )

            if saver.save_vacancy(vacancy):
                saved_count += 1

        print(f"   Сохранено вакансий: {saved_count}")
        total_vacancies += saved_count

    print(f"\n🎉 Сбор данных завершен! Всего сохранено вакансий: {total_vacancies}")


if __name__ == "__main__":
    main()
