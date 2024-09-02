from telebot.types import Message

from src.loader import bot


@bot.message_handler(func=lambda message: True)
async def echo_all(message: Message):
    """
    Функция ловит любое сообщение пользователя, пока у пользователя нет состояния
    """

    await bot.send_message(chat_id=message.chat.id, text='<i>Введите команду /help чтобы узнать возможности</i>')
