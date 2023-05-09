"""Валидация, используемая при CRUD операциях."""
from http import HTTPStatus

from fastapi import HTTPException
from pydantic import PositiveInt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject

from .constants import ERROR_MESSAGES


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    """Проврека на уникальность имени."""
    project_id = await charity_project_crud.get_project_id_by_name(project_name, session)
    if project_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ERROR_MESSAGES['name_dublicate'],
        )


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """Проверка наличия проекта с заданным id."""
    charity_project = await charity_project_crud.get(
        obj_id=project_id, session=session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=ERROR_MESSAGES['not_found'],
        )
    return charity_project


async def check_project_was_closed(
    project_id: int,
    session: AsyncSession,
):
    """Проврека актуальности проекта."""
    project_close_date = await session.execute(
        select(CharityProject.close_date).where(
            CharityProject.id == project_id
        )
    )
    project_close_date = project_close_date.scalars().first()
    if project_close_date:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ERROR_MESSAGES['project_was_closed']
        )


async def check_project_was_invested(
    project_id: int,
    session: AsyncSession,
):
    """Проврека наличия собранных средств у проекта."""
    db_project_invested_amount = await session.execute(
        select(CharityProject.invested_amount).where(
            CharityProject.id == project_id
        )
    )
    db_project_invested_amount = db_project_invested_amount.scalars().first()
    if db_project_invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ERROR_MESSAGES['project_was_invested']
        )


async def check_correct_full_amount_for_update(
    project_id: int,
    session: AsyncSession,
    full_amount_to_update: PositiveInt
):
    """Проврека поля количества собираемых средств перед изменением."""
    db_project_invested_amount = await session.execute(
        select(CharityProject.invested_amount).where(
            CharityProject.id == project_id
        )
    )
    db_project_invested_amount = db_project_invested_amount.scalars().first()
    if db_project_invested_amount > full_amount_to_update:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=ERROR_MESSAGES['incorrect_required_summ']
        )
