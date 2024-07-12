from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.crud.project import project_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB
from app.services.invest import investment_process


router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    response_model_exclude={
        'user_id',
        'invested_amount',
        'fully_invested',
        'close_date'
    }
)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Создание пожертвования."""
    new_donation = await donation_crud.create(donation, session, user)
    invest_process = investment_process(
        await project_crud.get_all_active(session),
        new_donation
    )
    session.add_all(invest_process)
    return await donation_crud.save(session, new_donation)


@router.get(
    '/',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперпользователя. Получение списка всех пожертвований."""
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
    response_model_exclude={
        'user_id',
        'invested_amount',
        'fully_invested',
        'close_date'
    }
)
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Получение списка всех пожертвований пользователя."""
    return await donation_crud.get_by_user(session, user)
