from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.fast_api.database.database import get_async_session
from .login_user import get_current_token_payload
from src.fast_api.schemas.habit import HabitPublicSchema
from src.fast_api.database import models


router = APIRouter(prefix='/jwt', tags=['JWT'])


@router.get('/user/me/habits', response_model=List[HabitPublicSchema])
async def get_habits(
        payload: dict = Depends(get_current_token_payload),
        db: AsyncSession = Depends(get_async_session),
):
    """
    Функция get запроса для получения всех привычек пользователя
    """

    tg_user_id: int = payload.get('tg_user_id')
    habits_in_db = await models.habit.Habit.get_habits_by_tg_user_id(tg_user_id=tg_user_id, db=db)

    if habits := habits_in_db.all():
        return habits

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Habits not found'
    )
