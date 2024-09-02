import httpx
from httpx import Response
from telebot.types import CallbackQuery

from src.bot.states.edit_habit_states import EditHabitState
from src.bot.utils_bot.get_user_jwt import get_header
from src.loader import bot, scheduler
from src.bot.keyboards.button_menu import menu_button
from config import settings


@bot.callback_query_handler(func=lambda call: call.data == 'performing_habit', state=EditHabitState.edite)
async def performing_habit(call: CallbackQuery):
    """
    Функция выполнение привычки, прибавляет счетчик привычки в базе данных postgres на стороне fast api
    """

    header: dict[str, str] | None = await get_header(call.from_user.id)

    if header:
        async with bot.retrieve_data(call.from_user.id) as data:
            title_habit: str = data['title_habit']
            del_msg_id: int = data['massage_id']
            del_chat_id: int = data['chat_id']

        async with httpx.AsyncClient() as client:
            response: Response = await client.patch(f'{settings.BASE_URL}/jwt/habit/performing/{title_habit}',
                                                    headers=header)

        if response.status_code == 204:

            if job := scheduler.get_job(job_id=f'{title_habit}'):
                job.remove()

            await bot.delete_message(message_id=del_msg_id, chat_id=del_chat_id)
            await bot.send_message(call.message.chat.id, f'<i>Привычка {title_habit} выполнена!</i>',
                                   reply_markup=menu_button())
            await bot.delete_state(user_id=call.from_user.id)
            return

        total_count: int = settings.total_count - response.json()['tracking_habit'][0]['count']
        await bot.send_message(call.message.chat.id, f'<i>Привычку "{title_habit}" осталось выполнить '
                                                     f'{total_count} раз</i>')
