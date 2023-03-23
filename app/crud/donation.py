from sqlalchemy import false, select
from app.models.donation import Donation
from app.crud.base import CRUDBase
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDDonation(CRUDBase):

    async def get_by_user(
        self,
        user: User,
        session: AsyncSession,
    ):
        donation = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        donation = donation.scalars().all()
        return donation

    async def get_all_not_closed_donations(
        self,
        session: AsyncSession,
    ):
        donation = await session.execute(
            select(Donation).where(
                Donation.fully_invested == false()
            ).order_by(Donation.create_date)
        )
        donation = donation.scalars().all()
        return donation


donation_crud = CRUDDonation(Donation)