from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.fast_api.database import models
from src.fast_api.database.database import get_async_session
from src.fast_api.schemas.habit import HabitPublicSchema
from .login_user import get_current_token_payload

router = APIRouter(prefix='/jwt', tags=['JWT'])


@router.get('/user/me/habit/{habit_title}', response_model=HabitPublicSchema)
async def get_habit(
        habit_title: str,
        payload: dict = Depends(get_current_token_payload),
        db: AsyncSession = Depends(get_async_session),
):
    """
    Функция get запроса для получения привычки
    """

    unauthed_exc: HTTPException = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="object not found",
    )
    tg_user_id: int = payload.get('tg_user_id')
    habit_in_db = await models.habit.Habit.get_habit_by_title(habit_title, tg_user_id, db=db)

    if habit_in_db is None:
        raise unauthed_exc

    return habit_in_db
