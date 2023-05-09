"""Модель базы данных для Пользователей."""
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """База данных для Пользователей."""
    pass
