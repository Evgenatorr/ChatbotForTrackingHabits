from sqlalchemy import select
from typing import Annotated
from fastapi import Depends, HTTPException, status, APIRouter
from jwt.exceptions import InvalidTokenError
from src.fast_api.database.database import get_async_session, AsyncSession
from config import settings
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials
from src.fast_api.utils.jwt_utils import encode_jwt, decode_jwt, validate_password
from src.fast_api import schemas
from src.fast_api import models


router = APIRouter(prefix='/jwt', tags=['JWT'])


async def validate_user(
        user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: AsyncSession = Depends(get_async_session),
):
    """
    Функция проверяет пользователя в базе данных проверяет пароль на валидность
    и возвращает пользователя, если данные валидны
    """

    user_in_db = await db.execute(select(models.user.User)
                                  .where(models.user.User.username == user_data.username))

    unauthed_exc: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )

    if (user := user_in_db.one_or_none()) is None:
        raise unauthed_exc

    if not validate_password(
            password=user_data.password,
            hashed_password=user[0].password
    ):
        raise unauthed_exc

    if not user[0].active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )

    return user[0]


async def get_current_token_payload(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(settings.security)]
) -> dict:
    """
    Функция проверяет токен на валидность и возвращает информацию о пользователе если он валиден
    """

    token: str = credentials.credentials

    try:
        payload: dict = decode_jwt(
            token=token,
        )

    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error",
        )

    return payload


async def get_current_auth_user(
        payload: dict = Depends(get_current_token_payload),
        db: AsyncSession = Depends(get_async_session),
) -> models.user.User:
    """
    Функция возвращает авторизованного пользователя
    """

    username: str = payload.get("username")
    tg_user_id: int = payload.get("tg_user_id")
    user_in_db = await models.user.User.get_user_by_username(username=username, tg_user_id=tg_user_id, db=db)

    if user_in_db:
        return user_in_db

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


def get_current_active_auth_user(
        user: schemas.user.UserOutSchema = Depends(get_current_auth_user),
) -> schemas.user.UserOutSchema:
    """
    Функция возвращает активного пользователя
    """

    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )


@router.post(path='/login', response_model=schemas.token.TokenInfo)
async def login(
        user: schemas.user.UserOutSchema = Depends(validate_user)
) -> schemas.token.TokenInfo:
    """
    Функция аутентификации пользователя и создания токена
    """

    jwt_payload = {
        'tg_user_id': user.tg_user_id,
        'username': user.username,
        'password': user.password.decode(),
    }

    token = encode_jwt(jwt_payload)

    return schemas.token.TokenInfo(
        access_token=token,
        token_type="Bearer",
    )
