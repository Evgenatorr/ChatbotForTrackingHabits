from src.loader import bot
from telebot.types import CallbackQuery
from src.bot.utils_bot.get_user_jwt import get_header
from src.bot import keyboards
from src.loader import scheduler
from src.bot.states.edit_habit_states import EditHabitState
from config import settings
import httpx


@bot.callback_query_handler(func=lambda call: call.data == 'delete_habit', state=EditHabitState.edite)
async def delete_habit(call: CallbackQuery):
    header = await get_header(call.from_user.id)
    async with bot.retrieve_data(call.from_user.id) as data:
        title_habit = data['title_habit']
        del_msg_id = data['massage_id']
        del_chat_id = data['chat_id']
    await bot.delete_message(message_id=del_msg_id, chat_id=del_chat_id)

    if header:
        async with httpx.AsyncClient() as client:
            response = await client.delete(f'{settings.BASE_URL}/jwt/habit/delete/{title_habit}',
                                          headers=header)
        if response.status_code == 204:
            if job := scheduler.get_job(job_id=f'{title_habit}'):
                job.remove()
            await bot.send_message(call.message.chat.id, f'<strong>Вы удалили привычку "{title_habit}"</strong>',
                                   reply_markup=keyboards.button_menu.menu_button())
        await bot.delete_state(call.from_user.id)
