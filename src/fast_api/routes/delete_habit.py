from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.fast_api.database import models
from src.fast_api.database.database import get_async_session
from .login_user import get_current_token_payload

router = APIRouter(prefix='/jwt', tags=['JWT'])


@router.delete('/habit/delete/{habit_title}',
               status_code=status.HTTP_204_NO_CONTENT,
               )
async def delete_habit(
        habit_title: str,
        db: AsyncSession = Depends(get_async_session),
        payload: dict = Depends(get_current_token_payload),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="object not found",
    )

    tg_user_id = payload.get('tg_user_id')
    habit_in_db = await models.habit.Habit.get_habit_by_title(habit_title, tg_user_id, db=db)

    if habit_in_db is None:
        raise unauthed_exc

    query = (
        delete(models.habit.Habit)
        .where(models.habit.Habit.title == habit_title)
    )

    await db.execute(query)
    await db.commit()
