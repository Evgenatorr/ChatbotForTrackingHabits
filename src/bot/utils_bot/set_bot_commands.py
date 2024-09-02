from telebot.async_telebot import AsyncTeleBot
from telebot.types import BotCommand

from config import settings


async def set_default_commands(bot: AsyncTeleBot):
    """
    Функция добавляет список команд для бота
    """

    await bot.set_my_commands(
        [BotCommand(*i) for i in settings.bot.default_commands]
    )
