import asyncio
from telebot.asyncio_filters import StateFilter
from src.bot.database.database import engine, Base
from src.bot.utils_bot.set_bot_commands import set_default_commands
from loader import bot


async def start():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await set_default_commands(bot)
    bot.add_custom_filter(StateFilter(bot))
    await bot.infinity_polling()


if __name__ == '__main__':
    asyncio.run(start())
