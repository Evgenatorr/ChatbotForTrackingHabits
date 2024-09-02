import httpx
from httpx import Response
from telebot.types import CallbackQuery, Message

from config import settings
from src.bot.keyboards.button_menu import menu_button
from src.bot.states.create_habit_states import CreateHabitState
from src.bot.utils_bot.get_user_jwt import get_header
from src.loader import bot


@bot.callback_query_handler(func=lambda call: call.data == 'create_habit')
async def new_habit(call: CallbackQuery) -> None:
    """
    Получаем название новой привычки от пользователя
    """

    header: dict[str, str] | None = await get_header(call.from_user.id)

    if header:
        await bot.set_state(call.from_user.id, state=CreateHabitState.add_title)
        async with bot.retrieve_data(user_id=call.from_user.id) as data:
            data['header'] = header

        await bot.send_message(call.message.chat.id, '<i>Введите название новой привычки</i>')


@bot.message_handler(state=CreateHabitState.add_title)
async def add_title_habit(message: Message) -> None:
    """
    Сохраняем название новой привычки от пользователя
    """

    await bot.set_state(message.from_user.id, state=CreateHabitState.add_description)
    async with bot.retrieve_data(message.from_user.id) as data:
        data['habit_title'] = message.text

    await bot.send_message(message.from_user.id, '<i>Введите описание новой привычки</i>')


@bot.message_handler(state=CreateHabitState.add_description)
async def add_description_habit(message: Message) -> None:
    """
    Принимаем описание новой привычки от пользователя
    и сохраняем данные в базе данных postgres на стороне fast api
    """

    async with bot.retrieve_data(message.from_user.id) as data:
        data['habit_description'] = message.text
        title_habit: str = data['habit_title']
        habit_info: dict[str, str | int] = {
            'user_id': message.from_user.id,
            'title': title_habit,
            'description': data['habit_description']
        }
        async with httpx.AsyncClient() as client:
            response: Response = await client.post(f'{settings.BASE_URL}/jwt/habit/create',
                                                   json=habit_info,
                                                   headers=data['header'])

    if response.status_code == 201:
        await bot.delete_state(message.from_user.id)
        await bot.send_message(message.from_user.id, f'<strong>Привычка "{title_habit}" добавлена</strong>',
                               reply_markup=menu_button())
        return

    elif response.status_code == 409:
        await bot.send_message(message.from_user.id, f'<i>Привычка "{title_habit}" уже существует</i>')
        await bot.delete_state(message.from_user.id)
