from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.fast_api.database.database import get_async_session
from .login_user import get_current_token_payload
from src.fast_api.schemas.habit import BaseHabitSchema, HabitPublicSchema
from src.fast_api.database import models

router = APIRouter(prefix='/jwt', tags=['JWT'])


@router.post('/habit/create', response_model=HabitPublicSchema)
async def create_habit(
        habit: BaseHabitSchema,
        db: AsyncSession = Depends(get_async_session),
        payload: dict = Depends(get_current_token_payload),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="object that already exists",
    )

    tg_user_id = payload.get('tg_user_id')
    habit_in_db = await models.user.Habit.get_habit_by_title(habit.title, tg_user_id)

    if habit_in_db:
        raise unauthed_exc

    habit_model = models.user.Habit(
        user_id=tg_user_id,
        title=habit.title,
        description=habit.description
    )

    db.add(habit_model)
    await db.flush()
    habit_tracking_model = models.user.HabitTracking(
        habit_id=habit_model.id,
    )

    db.add(habit_tracking_model)
    await db.commit()

    return habit_model
