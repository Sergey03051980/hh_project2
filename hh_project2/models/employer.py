# hh_project2/models/employer.py
from dataclasses import dataclass
from typing import Optional


@dataclass
class Employer:
    """Класс для представления работодателя"""
    id: int
    name: str
    url: Optional[str] = None
    description: Optional[str] = None
    vacancies_url: Optional[str] = None

    def __str__(self):
        return f"{self.name} (ID: {self.id})"

    def to_dict(self) -> dict:
        """Преобразует объект в словарь для БД"""
        return {
            "employer_id": self.id,
            "name": self.name,
            "url": self.url,
            "description": self.description
        }
