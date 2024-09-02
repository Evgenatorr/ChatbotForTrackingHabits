from datetime import datetime

from src.loader import bot
from telebot.types import CallbackQuery
from src.bot.utils_bot.get_user_jwt import get_header

from src.bot.states.edit_habit_states import EditHabitState
from dateutil.parser import parse
from config import settings
import httpx


@bot.callback_query_handler(func=lambda call: call.data == 'info_habit', state=EditHabitState.edite)
async def get_info_habit(call: CallbackQuery):
    """
    Функция выводит информацию по выбранной привычке
    """

    header: dict[str, str] | None = await get_header(call.from_user.id)

    if header:
        async with bot.retrieve_data(call.from_user.id) as data:
            title_habit = data['title_habit']

        async with httpx.AsyncClient() as client:
            response = await client.get(f'{settings.BASE_URL}/jwt/user/me/habit/{title_habit}',
                                        headers=header)

        alert_time: datetime.time | str = parse(response.json()['tracking_habit'][0]['alert_time']).time() \
            if response.json()['tracking_habit'][0]['alert_time'] else 'Не установлено'

        text = (f'<i>Название:</i> <strong>"{response.json()['title']}"</strong>\n'
                f'<i>Описание:</i> <strong>"{response.json()['description']}"</strong>\n'
                f'<i>Время ежедневного напоминания:</i> <strong>"{alert_time}"</strong>\n'
                f'<i>Выполнено:</i> <strong>{response.json()['tracking_habit'][0]['count']} дней</strong>')

        await bot.send_message(call.message.chat.id, text)
