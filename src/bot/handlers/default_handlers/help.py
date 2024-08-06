from telebot.types import Message
from config import settings
from src.loader import bot


@bot.message_handler(commands=["help"])
async def bot_help(message: Message):
    """
    Функция, которая ловит команду /help и выводит пользователю список всех команд
    """
    text = [f"/{command} - {desk}" for command, desk in settings.bot.default_commands]
    await bot.reply_to(message, "\n".join(text))
