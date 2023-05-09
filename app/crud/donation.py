"""Класс CRUD операций для Донатов."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation


class CRUDDonation(CRUDBase):
    """Класс CRUD операций для Доната."""

    async def get_by_user(
        self,
        user,
        session: AsyncSession,
    ) -> list[Donation]:
        """Получить id объекта по имени."""
        select_stmt = select(Donation).where(
            Donation.user_id == user.id,
        )
        donations = await session.execute(select_stmt)
        donations = donations.scalars().all()
        return donations


donation_crud = CRUDDonation(Donation)
