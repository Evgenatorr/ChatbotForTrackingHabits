from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Sequence
from src.fast_api import schemas
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.fast_api.database.database import get_async_session
from .login_user import get_current_token_payload, get_current_active_auth_user
from src.fast_api.schemas.habit import HabitPublicSchema
from src.fast_api.database import models


router = APIRouter(prefix='/jwt', tags=['JWT'])


@router.get('/user/me/habits', response_model=List[HabitPublicSchema])
async def get_habits(
        payload: dict = Depends(get_current_token_payload),
        db: AsyncSession = Depends(get_async_session),
):

    tg_user_id = payload.get('tg_user_id')
    habit_in_db = await db.execute(select(models.habit.Habit).where(
        models.habit.Habit.user_id == tg_user_id))

    if (habits := habit_in_db.scalars()) is not None:
        return habits.all()

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Habits not found'
    )