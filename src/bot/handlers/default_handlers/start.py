from os.path import split

from src.loader import bot
from telebot.types import Message, CallbackQuery
from src.bot.states.user_state import UserState
from config import settings
from src.bot import schemas
from src.bot.crud.create_token import insert_token_in_dblite
from src.bot.keyboards import button_login, button_menu
import httpx


@bot.message_handler(commands=['start'])
async def send_welcome(message: Message):
    await bot.send_message(message.chat.id, f'<strong>Войди | Зарегистрируйся</strong>',
                           reply_markup=button_login.login_and_reg_button())


@bot.callback_query_handler(func=lambda call: call.data == 'login')
async def login(call: CallbackQuery):
    await bot.set_state(call.from_user.id, UserState.login)
    await bot.send_message(chat_id=call.message.chat.id, text='<i>Введите логин, пароль (Через пробел)</i>')


@bot.message_handler(state=UserState.login)
async def check_login(message: Message):
    split_data_user = message.text.split()

    if len(split_data_user) != 2:
        await bot.reply_to(message, '<i>Введите логин, пароль (Через пробел)</i>')
        return

    data = {
        'username': split_data_user[0],
        'password': split_data_user[1]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url=f'{settings.BASE_URL}/jwt/login', data=data)

    if response.status_code == 401:
        await bot.send_message(message.chat.id, '<i>Не корректный логин или пароль</i>')
        return

    await bot.delete_message(message.chat.id, message.id)
    token_data = schemas.token.CreateToken(
        access_token=response.json()['access_token'],
        token_type=response.json()['token_type'],
        user_tg_id=message.from_user.id,
    )
    await insert_token_in_dblite(token_data)

    await bot.send_message(message.chat.id, '<strong>Вы вошли</strong>', reply_markup=button_menu.menu_button())
    await bot.delete_state(message.from_user.id, message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data == 'registration')
async def registration(call):
    await bot.set_state(call.from_user.id, UserState.registration)
    await bot.send_message(call.from_user.id, '<i>Придумайте логин, пароль (через пробел)</i>')


@bot.message_handler(state=UserState.registration)
async def check_login(message: Message):
    role = 'admin' if message.from_user.id == int(settings.TG_ADMIN_ID) else 'user'

    split_data_user = message.text.split()

    if len(split_data_user) != 2:
        await bot.reply_to(message, '<i>Придумайте логин, пароль (через пробел)</i>')
        return

    data = {
        'username': split_data_user[0],
        'password': split_data_user[1],
        'tg_user_id': message.from_user.id,
        'role': role,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f'{settings.BASE_URL}/registration', json=data)
    await bot.delete_message(message.chat.id, message.id)

    if response.status_code == 409:
        await bot.send_message(message.chat.id, f'<strong>Ты уже зарегистрирован</strong>',
                               reply_markup=button_login.login_button())
        await bot.delete_state(message.from_user.id, message.chat.id)
        return

    await bot.send_message(message.from_user.id, '<strong>Вы успешно зарегистрировались</strong>',
                           reply_markup=button_login.login_button())
    await bot.delete_state(message.from_user.id, message.chat.id)
