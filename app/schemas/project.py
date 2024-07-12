from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt, Field, Extra, validator


class ProjectCreate(BaseModel):
    """Схема для создания проекта."""
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class ProjectDB(ProjectCreate):
    """Схема для работы проектов с базой данных."""
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class ProjectUpdate(BaseModel):
    """Схема для обновления проекта."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    @validator('name')
    def name_cannot_be_null(cls, value):
        if not value:
            raise ValueError('Название проекта не может быть пустым!')
        return value

    @validator('description')
    def description_cannot_be_null(cls, value):
        if not value:
            raise ValueError('Описание проекта не может быть пустым!')
        return value

    class Config:
        extra = Extra.forbid
