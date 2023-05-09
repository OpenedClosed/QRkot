"""Модель базы данных для Донатов."""
from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import CommonBase


class Donation(CommonBase):
    """База данных для Донатов."""

    user_id = Column(Integer, ForeignKey(
        'user.id', name='fk_donation_user_id_user'
    ))
    comment = Column(Text)

    def __repr__(self):
        return (
            f'Было пожертвовано {self.full_amount} пользователем с id: {self.user_id}'
        )
