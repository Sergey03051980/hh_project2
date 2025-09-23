import os
from dotenv import load_dotenv

load_dotenv()

# Настройки базы данных
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'hh_project_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', ''),
    'port': os.getenv('DB_PORT', '5432')
}

# Настройки API
HH_API_URL = "https://api.hh.ru/"
COMPANIES = [
    {"id": 1740, "name": "Яндекс"},
    {"id": 15478, "name": "VK"},
    {"id": 3529, "name": "Сбер"},
    {"id": 4181, "name": "Ростелеком"},
    {"id": 1373, "name": "МТС"},
    {"id": 907345, "name": "Ozon"},
    {"id": 87021, "name": "Wildberries"},
    {"id": 39305, "name": "Альфа-Банк"}
]
