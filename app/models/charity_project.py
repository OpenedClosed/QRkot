"""Модель базы данных для Благотвроительных проектов."""
from sqlalchemy import Column, String, Text

from app.core.db import CommonBase


class CharityProject(CommonBase):
    """База данных для Благотворительных проектов."""

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (
            f'Cобрано {self.invested_amount}/{self.full_amount} на {self.name}'
        )
