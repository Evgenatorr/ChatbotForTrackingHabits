import httpx
from httpx import Response
from telebot.types import CallbackQuery

from config import settings
from src.bot import keyboards
from src.bot.states.edit_habit_states import EditHabitState
from src.bot.utils_bot.get_user_jwt import get_header
from src.loader import bot
from src.loader import scheduler


@bot.callback_query_handler(func=lambda call: call.data == 'delete_habit', state=EditHabitState.edite)
async def delete_habit(call: CallbackQuery):
    """
    Функция удаляет привычку из базы данных postgres на стороне fast api
    и удаляет напоминание этой привычки, если установлено
    """

    header: dict[str, str] | None = await get_header(call.from_user.id)

    async with bot.retrieve_data(call.from_user.id) as data:
        title_habit: str = data['title_habit']
        del_msg_id: int = data['massage_id']
        del_chat_id: int = data['chat_id']
    await bot.delete_message(message_id=del_msg_id, chat_id=del_chat_id)

    if header:
        async with httpx.AsyncClient() as client:
            response: Response = await client.delete(f'{settings.BASE_URL}/jwt/habit/delete/{title_habit}',
                                                     headers=header)

        if response.status_code == 204:
            if job := scheduler.get_job(job_id=f'{title_habit}'):
                job.remove()
            await bot.send_message(call.message.chat.id, f'<strong>Вы удалили привычку "{title_habit}"</strong>',
                                   reply_markup=keyboards.button_menu.menu_button())
        await bot.delete_state(call.from_user.id)
