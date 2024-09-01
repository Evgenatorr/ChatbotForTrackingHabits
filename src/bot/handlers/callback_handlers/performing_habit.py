from src.loader import bot
from telebot.types import CallbackQuery, Message
from src.bot.utils_bot.get_user_jwt import get_header
from src.bot.states.edit_habit_states import EditHabitState
from config import settings
import httpx


@bot.callback_query_handler(func=lambda call: call.data == 'performing_habit', state=EditHabitState.edite)
async def performing_habit(call: CallbackQuery):
    header = await get_header(call.from_user.id)

    if header:
        async with bot.retrieve_data(call.from_user.id) as data:
            title_habit = data['title_habit']
            del_msg_id = data['massage_id']
            del_chat_id = data['chat_id']

        async with httpx.AsyncClient() as client:
            response = await client.patch(f'{settings.BASE_URL}/jwt/habit/performing/{title_habit}',
                                          headers=header)

        if response.status_code == 204:
            await bot.send_message(call.message.chat.id, '<i>Ваша привычка выполнена 21 день</i>')
            await bot.delete_message(message_id=del_msg_id, chat_id=del_chat_id)
            return

        count_day = 21 - response.json()['tracking_habit'][0]['count']
        await bot.send_message(call.message.chat.id, f'<i>Осталось: {count_day} дней</i>')