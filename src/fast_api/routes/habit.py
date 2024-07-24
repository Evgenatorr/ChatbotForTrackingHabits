from fastapi import APIRouter, Depends
from src.fast_api import schemas
from .login_user import get_current_token_payload, get_current_active_auth_user

router = APIRouter(prefix='/jwt')


router.post('/habit/create')
def create_habit(
        payload: dict = Depends(get_current_token_payload),
        user: schemas.user.UserOut = Depends(get_current_active_auth_user),
):
    ...