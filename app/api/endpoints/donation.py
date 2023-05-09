"""Ручки, отвечающие за CRUD операции для Донатов."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.constants import MODEL_EXCLUDE_FIELDS
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB
from app.services.investing import start_investing

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude={*MODEL_EXCLUDE_FIELDS},
    response_model_exclude_none=True,
)
async def create_donation(
    donation_create: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Корутина создания Доната.
    Только для зарегистрированного пользователя."""
    new_donation = await donation_crud.create(
        donation_create, session, user
    )

    await start_investing(new_donation, charity_project_crud, session)

    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Корутина получения списка всех Донатов.
    Только для суперюзеров."""
    donations = await donation_crud.get_multi(session)
    return donations


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude={*MODEL_EXCLUDE_FIELDS},
)
async def get_my_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Корутина получения списка Донатов
    запрашивающего пользователя.
    Только для зарегистрированного пользователя."""
    donations = await donation_crud.get_by_user(
        user, session
    )
    return donations
