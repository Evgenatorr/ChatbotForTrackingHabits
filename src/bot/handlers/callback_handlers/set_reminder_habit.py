from src.loader import bot
from telebot.types import CallbackQuery, Message
from src.bot.utils_bot.get_user_jwt import get_header
from src.bot.states.edit_habit_states import EditHabitState
from config import settings
from src.loader import scheduler
from src.scheduler.scheduler import reminder_task
import httpx
import pytz
from httpx import Response
from dateutil.parser import parse


@bot.callback_query_handler(func=lambda call: call.data == 'set_reminder', state=EditHabitState.edite)
async def reminder(call: CallbackQuery):
    """
    Функция принимает время напоминания от пользователя
    """

    header: dict[str, str] | None = await get_header(call.from_user.id)

    if header:
        async with bot.retrieve_data(call.from_user.id) as data:
            data['header'] = header
        await bot.set_state(call.from_user.id, state=EditHabitState.save_reminder_time)
        await bot.send_message(call.message.chat.id, '<i>На какое время поставить ежедневное напоминание? '
                                                     'Пример(13:35)</i>')


@bot.message_handler(state=EditHabitState.save_reminder_time)
async def save_time(message: Message):
    """
    Функция сохраняет время напоминания от пользователя, добавляет это время в базу данных на стороне fast api,
    добавляет или изменяет задачу scheduler на указанное время
    """

    str_time: str = message.text

    async with bot.retrieve_data(message.from_user.id) as data:
        title_habit = data['title_habit']
        header: dict[str, str] = data['header']

    habit_data: dict[str, str] = {
        "alert_time": str_time
    }

    async with httpx.AsyncClient() as client:
        response: Response = await client.patch(f'{settings.BASE_URL}/jwt/habit/reminder/{title_habit}',
                                                headers=header, json=habit_data)

    if response.status_code == 400:
        await bot.send_message(message.chat.id, '<i>Не верный формат времени (Пример 20:40)</i>')
        return

    alert_time = parse(response.json()['alert_time'])

    if job := scheduler.get_job(job_id=f'{title_habit}'):
        job.reschedule('cron', hour=alert_time.hour,
                       minute=alert_time.minute,
                       timezone=pytz.timezone('Asia/Novosibirsk'))
        await bot.send_message(message.chat.id, f'<i>Вы изменили время напоминания на привычку "{title_habit}"\n'
                                                f'Время напоминания:</i> <strong>{alert_time.time()}</strong>')

        await bot.set_state(message.from_user.id, state=EditHabitState.edite)
        return

    scheduler.add_job(reminder_task, 'cron', hour=alert_time.hour,
                      minute=alert_time.minute,
                      timezone=pytz.timezone('Asia/Novosibirsk'), args=(message.chat.id, title_habit,),
                      id=f'{title_habit}')

    await bot.send_message(message.chat.id, f'<i>Вы установили ежедневное напоминание на привычку "{title_habit}"\n'
                                            f'Время ежедневного напоминания:</i> <strong>{alert_time.time()}</strong>')

    await bot.set_state(message.from_user.id, state=EditHabitState.edite)
