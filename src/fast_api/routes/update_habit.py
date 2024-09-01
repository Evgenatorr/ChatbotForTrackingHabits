from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from src.fast_api.database.database import get_async_session
from .login_user import get_current_token_payload, get_current_active_auth_user
from src.fast_api.schemas.habit import HabitUpdateSchema, HabitPublicSchema
from src.fast_api.database import models


router = APIRouter(prefix='/jwt', tags=['JWT'])


@router.patch('/habit/update/{habit_title}', response_model=HabitPublicSchema)
async def update_habit(
        habit_title: str,
        habit_update: HabitUpdateSchema,
        db: AsyncSession = Depends(get_async_session),
        payload: dict = Depends(get_current_token_payload),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="object not found",
    )

    conflict_exc = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="object that already exists",
    )

    tg_user_id = payload.get('tg_user_id')
    habit_in_db = await models.habit.Habit.get_habit_by_title(habit_title, tg_user_id, db=db)


    if habit_in_db is None:
        raise unauthed_exc

    if habit_update.title:
        check_title_in_db = await models.habit.Habit.get_habit_by_title(habit_update.title, tg_user_id, db=db)
        if check_title_in_db:
            raise conflict_exc

    habit_data = habit_update.model_dump(exclude_unset=True)
    print(habit_data)
    query = (
        update(models.habit.Habit)
        .where(models.habit.Habit.title == habit_title,
               models.habit.Habit.user_id == tg_user_id)
        .values(**habit_data)
        .returning(models.habit.Habit)
    )

    result = await db.execute(query)
    await db.commit()

    return result.scalar()
