from fastapi import APIRouter, Depends
from .login_user import get_current_token_payload, get_current_active_auth_user
from src.fast_api import schemas

router = APIRouter(prefix='/jwt', tags=['JWT'])


@router.get('/user/me')
async def read_users(
        payload: dict = Depends(get_current_token_payload),
        user: schemas.user.UserOutSchema = Depends(get_current_active_auth_user),
):

    iat = payload.get('iat')

    return {
        "username": user.username,
        "tg_user_id": user.tg_user_id,
        "logged_in_at": iat,
    }

