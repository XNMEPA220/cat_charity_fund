from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.models.user import User


class CRUDDonation(CRUDBase):
    """Класс для CRUD операций с пожертвованиями."""

    async def get_by_user(
            self,
            session: AsyncSession,
            user: User
    ):
        """Функция получения всех пожертвований пользователя."""
        reservation = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return reservation.scalars().all()


donation_crud = CRUDDonation(Donation)
