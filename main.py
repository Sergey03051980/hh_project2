#!/usr/bin/env python3
"""Основной модуль для запуска проекта."""

import asyncio
import sys
from pathlib import Path

# Добавляем корень проекта в Python path
sys.path.insert(0, str(Path(__file__).parent))

from hh_project2.api.hh_api import HeadHunterAPI
from hh_project2.database.db_creator import create_database, create_tables
from hh_project2.database.db_manager import DBManager
from hh_project2.utils.config import load_config


def main():
    """Основная функция запуска проекта."""
    print("🚀 Запуск HH Project 2.0")

    # Загрузка конфигурации
    config = load_config()
    print("✅ Конфигурация загружена")

    # Здесь будет основная логика
    print("Проект успешно инициализирован с Poetry!")

    # Пример использования API
    api = HeadHunterAPI()
    print("✅ API инициализировано")


if __name__ == "__main__":
    main()
