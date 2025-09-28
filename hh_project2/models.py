from dataclasses import dataclass
from typing import Optional

@dataclass
class Company:
    """Класс для представления компании"""
    id: int
    name: str
    description: Optional[str] = None
    url: Optional[str] = None

@dataclass
class Vacancy:
    """Класс для представления вакансии"""
    id: int
    name: str
    company_id: int
    salary_from: Optional[int] = None
    salary_to: Optional[int] = None
    currency: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
