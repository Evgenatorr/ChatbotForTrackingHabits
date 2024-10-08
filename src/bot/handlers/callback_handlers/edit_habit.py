from src.bot.keyboards.button_menu import menu_button
from src.loader import bot
from telebot.types import CallbackQuery, Message
from src.bot.utils_bot.get_user_jwt import get_header
from src.bot import keyboards
from src.loader import scheduler
from src.bot.states.edit_habit_states import EditHabitState
from config import settings
import httpx
from httpx import Response


@bot.callback_query_handler(func=lambda call: call.data == 'edit_habit', state=EditHabitState.edite)
async def choice_edit_habit(call: CallbackQuery) -> None:
    """
    Функция предоставляет выбор пользователю, изменить описание или название привычки
    """

    header: dict[str, str] | None = await get_header(call.from_user.id)

    if header:
        async with bot.retrieve_data(call.from_user.id) as data:
            data['header'] = header
            del_msg_id: int = data['massage_id']
            del_chat_id: int = data['chat_id']
        await bot.delete_message(message_id=del_msg_id, chat_id=del_chat_id)
        await bot.send_message(chat_id=call.message.chat.id, text='<strong>Что изменить</strong>',
                               reply_markup=keyboards.button_edit.choice_edit_habit())


@bot.callback_query_handler(func=lambda call: call.data == 'edit_description', state=EditHabitState.edite)
async def edit_description(call: CallbackQuery) -> None:
    """
    Функция принимает от пользователя новое описание привычки
    """

    await bot.set_state(call.from_user.id, state=EditHabitState.save_description)
    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.id,
                                text='<i>Введите новое описание</i>')


@bot.message_handler(state=EditHabitState.save_description)
async def save_description(message: Message) -> None:
    """
    Функция сохраняет новое описание привычки и изменяет данные в базе postgres на стороне fast api
    """

    async with bot.retrieve_data(message.from_user.id) as data:
        title_habit: str = data['title_habit']
        header: dict[str, str] = data['header']

    data = {
        'description': message.text
    }

    async with httpx.AsyncClient() as client:
        response = await client.patch(f'{settings.BASE_URL}/jwt/habit/update/{title_habit}',
                                      json=data,
                                      headers=header)

    if response.status_code == 200:
        await bot.send_message(message.chat.id, '<i>Вы изменили описание привычки</i>')
        await bot.delete_state(message.from_user.id)


@bot.callback_query_handler(func=lambda call: call.data == 'edit_title', state=EditHabitState.edite)
async def edit_title(call: CallbackQuery) -> None:
    """
    Функция принимает от пользователя новое название привычки
    """

    await bot.set_state(call.from_user.id, state=EditHabitState.save_title)
    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.id,
                                text='<i>Введите новое название</i>')


@bot.message_handler(state=EditHabitState.save_title)
async def save_title(message: Message) -> None:
    """
    Функция сохраняет новое название привычки и изменяет данные в базе postgres на стороне fast api
    """

    async with bot.retrieve_data(message.from_user.id) as data:
        title_habit: str = data['title_habit']
        header: dict[str, str] = data['header']

    new_title = message.text
    habit_data: dict[str, str] = {
        'title': new_title
    }

    async with httpx.AsyncClient() as client:
        response: Response = await client.patch(f'{settings.BASE_URL}/jwt/habit/update/{title_habit}',
                                                json=habit_data,
                                                headers=header)

    if response.status_code == 409:
        await bot.send_message(message.chat.id, '<i>Привычка с таким название уже существует\n'
                                                'Введите новое название</i>')
        return

    if job := scheduler.get_job(job_id=f'{title_habit}'):
        job.modify(id=new_title)

    await bot.delete_state(message.from_user.id)
    await bot.send_message(message.chat.id, '<strong>Вы изменили название привычки</strong>',
                           reply_markup=menu_button())
