"""Запуск бота"""

import time
import os
import asyncio
from telebot.asyncio_filters import StateFilter
from src.bot.database.database import engine, Base
from src.bot.utils_bot.set_bot_commands import set_default_commands
from src.loader import bot, scheduler


async def start():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    scheduler.start()
    await set_default_commands(bot)
    bot.add_custom_filter(StateFilter(bot))
    await bot.infinity_polling()


if __name__ == '__main__':
    os.environ['TZ'] = 'UTC'
    time.tzset()
    asyncio.run(start())
