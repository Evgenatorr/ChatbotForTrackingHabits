from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy import select
from src.fast_api.database.database import get_async_session, AsyncSession
from src.fast_api.utils.jwt_utils import hash_password
from src.fast_api import schemas
from src.fast_api import models

router = APIRouter(tags=['Registration'])


@router.post(path='/registration', response_model=schemas.user.UserOut)
async def reg_user(
        user: schemas.user.CreateUser,
        db: AsyncSession = Depends(get_async_session)
):
    user_in_db = await db.execute(select(models.user.User)
                                  .where(models.user.User.username == user.username))

    if user_in_db.one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This login already exists",
        )
    new_user = models.user.User(
        tg_user_id=user.tg_user_id,
        username=user.username,
        password=hash_password(user.password),
        role=user.role,
    )

    db.add(new_user)
    await db.commit()
    return new_user
