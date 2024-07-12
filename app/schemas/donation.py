from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt, Extra


class DonationCreate(BaseModel):
    """Схема для создания пожертвования."""
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationDB(DonationCreate):
    """Схема для работы пожертвований с базой данных."""
    id: int
    create_date: datetime
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
