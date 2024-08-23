from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from src.fast_api.database.database import get_async_session
from .login_user import get_current_token_payload, get_current_active_auth_user
from src.fast_api.schemas.habit import AddReminderSchema, HabitTrackingSchema
from src.fast_api.database import models
import datetime

router = APIRouter(prefix='/jwt', tags=['JWT'])


@router.patch('/habit/reminder/{habit_id}',
              status_code=status.HTTP_200_OK,
              )
async def add_reminder(
        habit_id: int,
        reminder_data: AddReminderSchema,
        db: AsyncSession = Depends(get_async_session),
        payload: dict = Depends(get_current_token_payload),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="object not found",
    )

    tg_user_id = payload.get('tg_user_id')
    habit_in_db = await models.user.Habit.get_habit_by_id(habit_id, tg_user_id)

    if habit_in_db is None:
        raise unauthed_exc
    reminder_data.alert_time = datetime.datetime.strptime(reminder_data.alert_time, '%H:%M')
    habit_data = reminder_data.model_dump(exclude_unset=True)

    query = (
        update(models.user.HabitTracking)
        .where(models.user.HabitTracking.habit_id == habit_id)
        .values(habit_data)
        .returning(models.user.HabitTracking)
    )

    result = await db.execute(query)
    await db.commit()
    return result.scalar()
