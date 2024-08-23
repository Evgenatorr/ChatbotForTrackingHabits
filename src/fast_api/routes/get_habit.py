from fastapi import APIRouter, Depends, HTTPException, status
from src.fast_api import schemas
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.fast_api.database.database import get_async_session
from .login_user import get_current_token_payload, get_current_active_auth_user
from src.fast_api.schemas.habit import BaseHabitSchema, HabitPublicSchema
from src.fast_api.database import models

router = APIRouter(prefix='/jwt', tags=['JWT'])


async def validate_title_habit(
        habit_title: str,
        payload: dict = Depends(get_current_token_payload)
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="object not found",
    )
    tg_user_id = payload.get('tg_user_id')
    habit_in_db = await models.user.Habit.get_habit_by_title(habit_title, tg_user_id)

    if habit_in_db is None:
        raise unauthed_exc

    return habit_in_db


@router.get('/user/me/habit', response_model=HabitPublicSchema)
async def get_habit(
        habit: BaseHabitSchema = Depends(validate_title_habit),
):

    return habit
