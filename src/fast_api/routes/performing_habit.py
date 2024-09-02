from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.fast_api.database.database import get_async_session
from .login_user import get_current_token_payload
from src.fast_api.database import models
from config import settings

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
    """
    Функция patch запроса для выполнения привычки, прибавляем счетчик выполнения привычки в базе данных
    и удаляем привычку если счетчик больше total_count(количество выполнения
    привычки перед тем как она будет удалена, настраивается в 'config.py')
    """

    notfound_exc = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Object not found",
    )

    no_content_exc = HTTPException(
        status_code=status.HTTP_204_NO_CONTENT,
        detail="Object deleted",
    )

    tg_user_id: int = payload.get('tg_user_id')
    habit_in_db = await models.habit.Habit.get_habit_by_title(habit_title, tg_user_id, db=db)

    if habit_in_db is None:
        raise notfound_exc

    habit_in_db.tracking_habit[0].count += 1

    if habit_in_db.tracking_habit[0].count >= settings.total_count:
        await db.delete(habit_in_db)
        await db.commit()
        raise no_content_exc

    await db.commit()

    return habit_in_db
