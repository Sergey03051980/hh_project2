import os
from dotenv import load_dotenv

load_dotenv()

# Настройки для подключения к основной БД (для создания новой БД)
DEFAULT_DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': 'postgres',  # Подключаемся к стандартной БД
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', ''),
    'port': os.getenv('DB_PORT', '5432')
}

# Настройки для рабочей БД (будет создана)
WORK_DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'hh_db'),  # Новая БД
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', ''),
    'port': os.getenv('DB_PORT', '5432')
}

# Название новой БД
DB_NAME = os.getenv('DB_NAME', 'hh_db')

# Настройки API
HH_API_URL = "https://api.hh.ru/"
COMPANIES = [
    {"id": 1740, "name": "Яндекс"},
    {"id": 15478, "name": "VK"},
    {"id": 3529, "name": "Сбер"},
    {"id": 4181, "name": "Ростелеком"},
    {"id": 1373, "name": "МТС"},
    {"id": 907345, "name": "Ozon"},
    {"id": 4934, "name": "Билайн"},
    {"id": 1057, "name": "Касперский"},
    {"id": 87021, "name": "Wildberries"},
    {"id": 39305, "name": "Альфа-Банк"}
]
