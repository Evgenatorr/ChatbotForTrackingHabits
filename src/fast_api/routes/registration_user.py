from fastapi import Depends, HTTPException, status, APIRouter

from src.fast_api import models
from src.fast_api import schemas
from src.fast_api.database.database import get_async_session, AsyncSession
from src.fast_api.utils.jwt_utils import hash_password

router = APIRouter(tags=['Registration'])


@router.post(path='/registration', response_model=schemas.user.BaseUserSchema)
async def reg_user(
        user: schemas.user.CreateUserSchema,
        db: AsyncSession = Depends(get_async_session),
):
    """
    Функция post запроса, добавляем нового пользователя в базу данных если такого уже нет
    """

    user_in_db = await models.user.User.get_user_by_username(
        username=user.username,
        tg_user_id=user.tg_user_id,
        db=db,
    )

    if user_in_db is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This tg id already exists",
        )

    new_user: models.user.User = models.user.User(
        tg_user_id=user.tg_user_id,
        username=user.username,
        password=hash_password(user.password),
    )

    db.add(new_user)
    await db.commit()

    return new_user
