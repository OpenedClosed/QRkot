"""Описание процесса инвестирования, исполняемого при
создании объекта Благотвроительно проекта или Доаната."""
from datetime import datetime
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base


def close_investing(objs: List[Base]) -> None:
    """Закрытие благотворительных проектов или донатов."""
    for obj in objs:
        obj.fully_invested = (obj.full_amount == obj.invested_amount)
        if obj.fully_invested:
            obj.close_date = datetime.now()


async def start_investing(
    new_obj: Base,
    old_obj: Base,
    session: AsyncSession
) -> None:
    """Корутина запуска процесса инвестирования."""

    investments = await old_obj.get_not_fully_invested(session)

    for invest in investments:
        need_for_invest = new_obj.full_amount - new_obj.invested_amount
        free_sum = invest.full_amount - invest.invested_amount
        investing_amount = min(need_for_invest, free_sum)
        invest.invested_amount += investing_amount
        new_obj.invested_amount += investing_amount
        data_for_potential_closing = [invest, new_obj]
        close_investing(data_for_potential_closing)
    await session.commit()
