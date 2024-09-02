from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.fast_api.database import models
from src.fast_api.database.database import get_async_session
from src.fast_api.schemas.habit import BaseHabitSchema, HabitPublicSchema
from .login_user import get_current_token_payload

router = APIRouter(prefix='/jwt', tags=['JWT'])


@router.post('/habit/create', response_model=HabitPublicSchema, status_code=status.HTTP_201_CREATED)
async def create_habit(
        habit: BaseHabitSchema,
        db: AsyncSession = Depends(get_async_session),
        payload: dict = Depends(get_current_token_payload),
):
    """
    Функция post запроса для добавления новой привычки в базу данных
    """

    unauthed_exc: HTTPException = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="object that already exists",
    )

    tg_user_id: int = payload.get('tg_user_id')
    habit_in_db = await models.habit.Habit.get_habit_by_title(habit.title, tg_user_id, db=db)

    if habit_in_db:
        raise unauthed_exc

    habit_model: models.habit.Habit = models.habit.Habit(
        user_id=tg_user_id,
        title=habit.title,
        description=habit.description
    )

    db.add(habit_model)
    await db.flush()

    habit_tracking_model: models.habit.HabitTracking = models.habit.HabitTracking(
        habit_id=habit_model.id,
    )
    db.add(habit_tracking_model)
    await db.refresh(habit_model)
    await db.commit()
    return habit_model
