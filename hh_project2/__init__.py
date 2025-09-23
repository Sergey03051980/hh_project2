"""
HH Project 2.0 - Парсинг вакансий с hh.ru
"""

__version__ = "1.0.0"
__author__ = "Your Name"

from .api import HHAPI
from .database import DatabaseManager
from .db_manager import DBManager
from .models import Company, Vacancy
