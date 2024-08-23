from src.loader import bot
from telebot.types import CallbackQuery, Message
from src.bot.utils_bot.get_user_jwt import get_header
from src.bot.states.create_habit_states import CreateHabitState
from config import settings
import httpx


@bot.callback_query_handler(func=lambda call: call.data == 'update_habit')
async def update_habit(call: CallbackQuery):
    header = await get_header(call.from_user.id)

    if header:
        await bot.set_state(call.from_user.id, state=CreateHabitState.add_title)
        async with bot.retrieve_data(user_id=call.from_user.id) as data:
            data['header'] = header

        await bot.send_message(call.message.chat.id, 'Введите название новой привычки:')


@bot.message_handler(state=CreateHabitState.add_title)
async def add_title_habit(message: Message):
    await bot.set_state(message.from_user.id, state=CreateHabitState.add_description)
    async with bot.retrieve_data(message.from_user.id) as data:
        data['habit_title'] = message.text

    await bot.send_message(message.from_user.id, "Введите описание новой привычки:")


@bot.message_handler(state=CreateHabitState.add_description)
async def add_description_habit(message: Message):
    async with bot.retrieve_data(message.from_user.id) as data:
        data['habit_description'] = message.text
        habit_info = {
            'user_id': message.from_user.id,
            'title': data['habit_title'],
            'description': data['habit_description']
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(f'{settings.BASE_URL}/jwt/habit/create',
                                         json=habit_info,
                                         headers=data['header'])
    print(response.status_code, response.json())
    if response.status_code == 200:
        await bot.send_message(message.from_user.id, "Привычка добавлена")
        bot.delete_state(message.from_user.id)
        return
    elif response.status_code == 409:
        await bot.send_message(message.from_user.id, "Такая привычка уже добавлена")