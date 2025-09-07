# tests/test_api.py
from hh_project2.api.hh_api import HeadHunterAPI


def test_api():
    api = HeadHunterAPI()

    # Тестируем получение работодателя
    employer = api.get_employer(1455)  # HeadHunter
    if employer:
        print(f"✅ Работодатель: {employer.get('name')}")
        print(f"   URL: {employer.get('alternate_url')}")
    else:
        print("❌ Не удалось получить работодателя")
        return

    # Тестируем вакансии
    vacancies = api.get_all_vacancies(1455, max_pages=1)
    print(f"✅ Получено вакансий: {len(vacancies)}")

    # Покажем первые 5 вакансий если есть
    if vacancies:
        print("\nПервые 5 вакансий:")
        for i, vacancy in enumerate(vacancies[:5]):
            salary = vacancy.get('salary')
            if salary:
                salary_info = f"{salary.get('from', '?')}-{salary.get('to', '?')} {salary.get('currency', '')}"
            else:
                salary_info = "не указана"

            print(f"{i + 1}. {vacancy.get('name')}")
            print(f"   Зарплата: {salary_info}")
            print(f"   URL: {vacancy.get('alternate_url')}")
            print()


if __name__ == "__main__":
    test_api()
