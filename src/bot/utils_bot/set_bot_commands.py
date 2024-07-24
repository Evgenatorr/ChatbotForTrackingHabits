"""
Модуль добавления команд для бота
"""

from telebot.types import BotCommand
from config import settings


async def set_default_commands(bot):
    await bot.set_my_commands(
        [BotCommand(*i) for i in settings.bot.default_commands]
    )
