# main.py
print("🚀 Запуск HH Project 2.0 с Poetry!")

try:
    import requests
    from dotenv import load_dotenv

    print("✅ Все пакеты загружены успешно!")

    # Загружаем конфигурацию
    from hh_project2.utils.config import load_config

    config = load_config()
    print("✅ Конфигурация загружена")

    # Тест API
    response = requests.get("https://api.hh.ru/", timeout=5)
    print(f"✅ API hh.ru доступно, статус: {response.status_code}")

    # Показываем конфиг
    db_config = config["db"]
    print(f"   DB: {db_config['user']}@{db_config['host']}:{db_config['port']}")

except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback

    traceback.print_exc()
