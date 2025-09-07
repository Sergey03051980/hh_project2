# hh_project2/utils/config.py
import os
from dotenv import load_dotenv
from typing import Dict, Any

def load_dotenv_config():
    """Загружает переменные окружения из .env файла"""
    load_dotenv()

def get_db_config() -> Dict[str, Any]:
    """Возвращает конфигурацию для подключения к БД"""
    return {
        "database": os.getenv("DB_NAME", "hh_vacancies"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", ""),
        "host": os.getenv("DB_HOST", "localhost"),
        "port": os.getenv("DB_PORT", "5432")
    }

def get_api_config() -> Dict[str, Any]:
    """Возвращает конфигурацию для API"""
    return {
        "base_url": "https://api.hh.ru",
        "user_agent": "HH-API-Project/1.0 (serzh466163@gmail.com)",
        "delay": 0.2
    }

# Функция load_config для обратной совместимости
def load_config() -> Dict[str, Any]:
    """Загружает всю конфигурацию (для обратной совместимости)"""
    load_dotenv_config()
    return {
        "db": get_db_config(),
        "api": get_api_config()
    }

# Константа для обратной совместимости
DB_CONFIG = get_db_config()
