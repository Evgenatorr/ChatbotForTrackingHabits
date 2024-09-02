import httpx
from httpx import Response
from telebot.types import CallbackQuery

from config import settings
from src.bot.states.edit_habit_states import EditHabitState
from src.bot.utils_bot.get_user_jwt import get_header
from src.loader import bot
from src.loader import scheduler


@bot.callback_query_handler(func=lambda call: call.data == 'delete_reminder', state=EditHabitState.edite)
async def delete_reminder(call: CallbackQuery) -> None:
    """
    Функция удаляет напоминание у привычки из хранилища задач "apscheduler"
    и меняет значение alert_time в таблице tracking_habit на стороне fast api на null
    """

    header: dict[str, str] | None = await get_header(call.from_user.id)

    if header:
        async with bot.retrieve_data(call.from_user.id) as data:
            title_habit = data['title_habit']

        if job := scheduler.get_job(job_id=f'{title_habit}'):
            job.remove()

            data = {
                "alert_time": None
            }

            async with httpx.AsyncClient() as client:
                response: Response = await client.patch(f'{settings.BASE_URL}/jwt/habit/reminder/{title_habit}',
                                                        headers=header, json=data)

            await bot.send_message(call.message.chat.id, f'<i>Напоминание на привычку "{title_habit}" удалено</i>')
            return

        await bot.send_message(call.message.chat.id, f'<i>Напоминание на привычку "{title_habit}" не установлено</i>')
