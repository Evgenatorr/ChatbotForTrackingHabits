from src.loader import bot
from telebot.types import CallbackQuery, Message
from src.bot.utils_bot.get_user_jwt import get_header
from src.bot.states.edit_habit_states import EditHabitState
from src.bot import keyboards
from config import settings
import httpx


@bot.callback_query_handler(func=lambda call: call.data == 'list_habit')
async def list_habit(call: CallbackQuery):
    header = await get_header(call.from_user.id)

    if header:
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{settings.BASE_URL}/jwt/user/me/habits', headers=header)

        if response.status_code == 404:
            await bot.send_message(call.message.chat.id, '<i>У вас пока нет созданных привычек</i>')
            return

        habits: list = [habit['title'] for habit in response.json()]

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                    text='<strong>Выберите привычку</strong>',
                                    reply_markup=keyboards.button_habit.habit_button(habits))


@bot.callback_query_handler(func=lambda call: call.data.startswith('title_'))
async def list_habit(call: CallbackQuery):
    title_habit = call.data[6:]
    await bot.set_state(call.from_user.id, state=EditHabitState.edite)

    async with bot.retrieve_data(call.from_user.id) as data:
        data['title_habit'] = title_habit
        data['massage_id'] = call.message.id
        data['chat_id'] = call.message.chat.id

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                text=f'<strong>Выберите действие для привычки</strong> "{title_habit}"',
                                reply_markup=keyboards.button_edit.edit_button())
