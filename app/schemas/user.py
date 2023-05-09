"""Модель схемы данных запроса для Пользователя."""
from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Базовая схема данных запроса для Пользователя."""
    pass


class UserCreate(schemas.BaseUserCreate):
    """Схема данных запроса для создания Пользователя."""
    pass


class UserUpdate(schemas.BaseUserUpdate):
    """Схема данных запроса для обновления Пользователя."""
    pass
