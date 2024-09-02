from datetime import datetime
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from sqlalchemy.sql.dml import ReturningUpdate
from sqlalchemy import Result

from src.fast_api.database.database import get_async_session
from .login_user import get_current_token_payload
from src.fast_api.schemas.habit import SetReminderSchema, HabitTrackingSchema
from src.fast_api.database import models
import pytz


router = APIRouter(prefix='/jwt', tags=['JWT'])


@router.patch(
    '/habit/reminder/{habit_title}',
    status_code=status.HTTP_200_OK,
    response_model=HabitTrackingSchema
)
async def add_reminder(
        habit_title: str,
        reminder_data: SetReminderSchema,
        db: AsyncSession = Depends(get_async_session),
        payload: dict = Depends(get_current_token_payload),
):
    """
    Функция patch запроса, добавляем время уведомления в базу данных
    """

    notfound_exc: HTTPException = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Object not found",
    )

    value_time_exc: HTTPException = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid time format",
    )

    tg_user_id: int = payload.get('tg_user_id')
    habit_in_db: models.habit.Habit | None = await models.habit.Habit.get_habit_by_title(
        habit_title, tg_user_id, db=db
    )

    if habit_in_db is None:
        raise notfound_exc

    if reminder_data.alert_time is None:
        habit_in_db.tracking_habit[0].alert_time = None
        await db.commit()
        return habit_in_db.tracking_habit[0]

    try:
        reminder_data.alert_time = datetime.strptime(reminder_data.alert_time, '%H:%M').replace(
            tzinfo=pytz.timezone('Asia/Novosibirsk'))
    except ValueError:
        raise value_time_exc

    habit_data: dict[str, Any] = reminder_data.model_dump(exclude_unset=True)

    query: ReturningUpdate[tuple[models.habit.HabitTracking]] = (
        update(models.habit.HabitTracking)
        .where(models.habit.HabitTracking.habit_id == habit_in_db.id)
        .values(habit_data)
        .returning(models.habit.HabitTracking)
    )

    result: Result[tuple[models.habit.HabitTracking]] = await db.execute(query)

    await db.commit()
    return result.scalar()
