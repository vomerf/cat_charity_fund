from typing import List
from fastapi import APIRouter, Depends
from app.core.db import get_async_session
# from app.crud.donation import create_donation, get_all_donations_from_db
from app.schemas.donation import DonationDB, DonationCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.donation import donation_crud
from app.core.user import current_user, current_superuser
from app.models import User
from app.services.invest import invest

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    response_model_exclude={
        'invested_amount',
        'fully_invested',
        'close_date',
        'user_id'
    },
)
async def create_new_charityproject(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):

    new_donation = await donation_crud.create(donation, session, user)
    new_donation = await invest(session, new_donation)
    return new_donation


@router.get(
    '/',
    response_model=List[DonationDB],
    dependencies=[Depends(current_superuser)],
    response_model_exclude={'close_date'}
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get(
    '/my',
    response_model=List[DonationDB],
    response_model_exclude={
        'invested_amount',
        'fully_invested',
        'close_date',
        'user_id',
    },
)
async def get_all_my_donation(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    donation = await donation_crud.get_by_user(user, session)
    return donation