from loader import bot
from telebot.types import Message
from config import settings
from src.bot.handlers.default_handlers.start import session


@bot.message_handler(commands=['info'])
async def info(message: Message):
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        print(data)
        if data is None:
            await bot.send_message(message.chat.id, 'Войдите в аккаунт')
        response = session.get(f'{settings.BASE_URL}/info', headers=data)
    result = f'Логин: {response.json()['username']}\n'
    await bot.send_message(message.chat.id, result)
