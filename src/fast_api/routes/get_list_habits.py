from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Sequence
from src.fast_api import schemas
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.fast_api.database.database import get_async_session
from .login_user import get_current_token_payload, get_current_active_auth_user
from src.fast_api.schemas.habit import HabitPublicSchema
from src.fast_api.database import models
from ..database.models.user import Habit

router = APIRouter(prefix='/jwt', tags=['JWT'])


async def get_current_auth_user_list_habit(
        payload: dict = Depends(get_current_token_payload),
        db: AsyncSession = Depends(get_async_session),
) -> Sequence[Habit]:
    tg_user_id = payload.get('tg_user_id')
    habit_in_db = await db.execute(select(models.user.Habit).where(
        models.user.Habit.user_id == tg_user_id))

    if (habits := habit_in_db.scalars()) is not None:
        return habits.all()

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='token invalid (user not found)',
    )


@router.get('/user/me/habits', response_model=List[HabitPublicSchema])
async def create_habit(
        habits: List[HabitPublicSchema] = Depends(get_current_auth_user_list_habit),
):
    if len(habits) > 0:
        return habits

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Habits not found'
    )