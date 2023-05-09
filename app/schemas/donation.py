"""Модель схемы данных запроса для Доната."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class DonationBase(BaseModel):
    """Базовая схема данных запроса для Доната."""
    comment: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    """Схема данных запроса для создания Доната."""
    full_amount: PositiveInt


class DonationDB(DonationCreate):
    """Схема данных запроса содержащая
    все поля Доната."""
    id: int
    user_id: Optional[int]
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
