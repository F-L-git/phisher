# src/phisher/models/perimeter.py
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional


class Perimeter(BaseModel):
    """
    Модель для валидации JSON-файла с описанием защищаемого периметра.
    """
    domains: List[str] = Field(..., description="Эталонные домены организации")
    topdomains: List[str] = Field(...,
                                  description="Легитимные домены верхнего уровня")
    brandnames: List[str] = Field(...,
                                  description="Названия брендов для поиска субдоменов")
    whois: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Ожидаемые данные WHOIS (ключи: organisation, phone, email)"
    )
    keywords: List[str] = Field(
        default_factory=list,
        description="Ключевые слова для поиска на страницах"
    )
    imglinks: List[str] = Field(
        default_factory=list,
        description="Ссылки на официальные изображения (логотипы, баннеры)"
    )

    # Опционально: валидаторы для формата доменов
    @validator('domains', 'topdomains', 'brandnames', each_item=True)
    def check_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Пустые строки не допускаются")
        return v

    # Можно добавить проверку, что все домены валидны (но это сложнее, оставим на потом)

    class Config:
        # Разрешаем дополнительные поля, но лучше запретить, чтобы не пропускать ошибки
        extra = "forbid"
