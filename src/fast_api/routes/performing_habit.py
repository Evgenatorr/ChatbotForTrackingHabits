from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from src.fast_api.database.database import get_async_session
from .login_user import get_current_token_payload, get_current_active_auth_user
from src.fast_api.schemas.habit import SetReminderSchema, HabitTrackingSchema
from src.fast_api.database import models



router = APIRouter(prefix='/jwt', tags=['JWT'])


@router.patch(
    '/habit/performing/{habit_title}',
    status_code=status.HTTP_200_OK,
)
async def performing_habit(
        habit_title: str,
        db: AsyncSession = Depends(get_async_session),
        payload: dict = Depends(get_current_token_payload),
):
    notfound_exc = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Object not found",
    )

    no_content_exc = HTTPException(
        status_code=status.HTTP_204_NO_CONTENT,
        detail="Object deleted",
    )

    tg_user_id = payload.get('tg_user_id')
    habit_in_db: models.habit.Habit = await models.habit.Habit.get_habit_by_title(habit_title, tg_user_id, db=db)

    if habit_in_db is None:
        raise notfound_exc

    habit_in_db.tracking_habit[0].count += 1

    if habit_in_db.tracking_habit[0].count > 20:
        await db.delete(habit_in_db)
        await db.commit()
        raise no_content_exc

    await db.commit()

    return habit_in_db
