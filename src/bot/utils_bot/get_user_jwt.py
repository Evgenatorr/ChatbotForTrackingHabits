from src.bot.database import models
import httpx
from config import settings
from src.loader import bot
from src.bot.keyboards import button_login


async def get_header(user_tg_id: int):
    token = await models.Token.get_token_by_user_id(user_tg_id)

    if token:

        header = {
            'Authorization': f'{token.token_type} {token.access_token}'
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url=f'{settings.BASE_URL}/jwt/user/me', headers=header)

        if response.status_code == 401:
            await bot.send_message(user_tg_id, 'Войдите', reply_markup=button_login.login_button())
            return

        return header
    else:
        await bot.send_message(user_tg_id, 'Войдите', reply_markup=button_login.login_button())
