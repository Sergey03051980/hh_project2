# hh_project2/models/vacancy.py
from dataclasses import dataclass
from typing import Optional


@dataclass
class Vacancy:
    """Класс для представления вакансии"""
    id: int
    employer_id: int
    title: str
    salary_from: Optional[int] = None
    salary_to: Optional[int] = None
    currency: Optional[str] = None
    url: Optional[str] = None
    requirement: Optional[str] = None
    responsibility: Optional[str] = None

    def __str__(self):
        salary_info = ""
        if self.salary_from or self.salary_to:
            salary_info = f", Зарплата: {self.salary_from or '?'}-{self.salary_to or '?'} {self.currency or ''}"
        return f"{self.title}{salary_info}"

    def to_dict(self) -> dict:
        """Преобразует объект в словарь для БД"""
        return {
            "vacancy_id": self.id,
            "employer_id": self.employer_id,
            "title": self.title,
            "salary_from": self.salary_from,
            "salary_to": self.salary_to,
            "currency": self.currency,
            "url": self.url,
            "requirement": self.requirement,
            "responsibility": self.responsibility
        }
