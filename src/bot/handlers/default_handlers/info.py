from src.loader import bot
from telebot.types import CallbackQuery
from src.bot.utils_bot.get_user_jwt import get_header
from src.bot.keyboards import button_login


@bot.callback_query_handler(func=lambda call: call.data == 'info')
async def info(call: CallbackQuery):
    user = await get_header(call.from_user.id)

    if user:

        result = f'Логин: {user['username']}'
        await bot.send_message(call.message.chat.id, result)
        return

    await bot.send_message(
        call.message.chat.id, 'Войдите или зарегистрируйтесь',
        reply_markup=button_login.login_button()
    )
