from src.loader import bot
from telebot.types import CallbackQuery, Message
from src.bot.utils_bot.get_user_jwt import get_header
from src.bot.keyboards.button_edit import edit_button
from src.bot.keyboards.button_habit import habit_button
from src.bot.states.edit_habit_states import EditHabitState
from config import settings
import httpx


# @bot.callback_query_handler(func=lambda call: call.data == 'habit_edit')
# async def edit_habit(call: CallbackQuery):
#     header = await get_header(call.from_user.id)
#
#     if header:
#         bot.set_state(call.from_user.id, state=EditHabitState.title)
#         await bot.send_message(call.message.chat.id, 'Введите название привычки')
#
#
# @bot.message_handler(state=EditHabitState.title)
# async def check_title_habit(message: Message):
#
#     habit_data = {
#         'tg_user_id': message.from_user.id,
#         'title': message.text
#     }
#
#
#     async with httpx.AsyncClient() as client:
#         response = await client.post(f'{settings.BASE_HOST}/jwt/user/me/habit', json=habit_data)


@bot.callback_query_handler(func=lambda call: call.data == 'habit_edit')
async def edit_habit(call: CallbackQuery):
    header = await get_header(call.from_user.id)

    if header:
        async with httpx.AsyncClient() as client:
            client.get()
        bot.set_state(call.from_user.id, state=EditHabitState.title)
        await bot.send_message(call.message.chat.id, 'Выберите привычку', reply_markup=habit_button(header))


@bot.callback_query_handler(state=EditHabitState.title, func=lambda call: True)
async def check_title_habit(call: CallbackQuery):

    habit_data = {
        'tg_user_id': call.from_user.id,
        'title': call.message.text
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f'{settings.BASE_HOST}/jwt/user/me/habit', json=habit_data)
