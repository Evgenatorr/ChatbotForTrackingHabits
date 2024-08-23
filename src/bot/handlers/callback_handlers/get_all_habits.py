from src.loader import bot
from telebot.types import CallbackQuery, Message
from src.bot.utils_bot.get_user_jwt import get_header
from src.bot.states.create_habit_states import CreateHabitState
from config import settings
import httpx


@bot.callback_query_handler(func=lambda call: call.data == 'list_habit')
async def list_habit(call: CallbackQuery):
    header = await get_header(call.from_user.id)

    if header:
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{settings.BASE_URL}/jwt/user/me/habits', headers=header)

        if response.status_code == 404:
            await bot.send_message(call.message.chat.id, 'У вас пока нет созданных привычек')
            return

        result = ''.join(
            [
                f'Привычка: {habit['title']} Описание: {habit['description']}\n'
                for habit in response.json()
            ]
        )

        await bot.send_message(call.message.chat.id, result)
