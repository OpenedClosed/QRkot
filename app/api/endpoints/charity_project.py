"""Ручки, отвечающие за CRUD операции для Благотвротиельного Проекта."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_exists,
                                check_correct_full_amount_for_update,
                                check_name_duplicate, check_project_was_closed,
                                check_project_was_invested)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investing import start_investing

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_project(
    charity_project_create: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Корутина создания Благотвроительного проекта.
    Только для суперюзеров."""
    await check_name_duplicate(charity_project_create.name, session)

    new_project = await charity_project_crud.create(
        charity_project_create,
        session
    )
    await start_investing(new_project, donation_crud, session)

    await session.refresh(new_project)
    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Корутина получения списка Благотвроительных проектов."""
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_project(
    charity_project_id: int,
    charity_project_update: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Корутина изменения данных Благотворительного проекта.
    Только для суперюзеров."""
    charity_project = await check_charity_project_exists(
        charity_project_id,
        session
    )
    await check_project_was_closed(charity_project_id, session)

    if charity_project_update.full_amount is not None:
        await check_correct_full_amount_for_update(
            charity_project_id, session, charity_project_update.full_amount
        )

    if charity_project_update.name is not None:
        await check_name_duplicate(charity_project_update.name, session)

    charity_project = await charity_project_crud.update(
        charity_project, charity_project_update, session
    )
    return charity_project


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_meeting_room(
    charity_project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Корутина удаления Благотворительного проекта.
    Только для суперюзеров."""
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )

    await check_project_was_invested(charity_project_id, session)

    charity_project = await (
        charity_project_crud.remove(
            charity_project, session
        )
    )
    return charity_project
