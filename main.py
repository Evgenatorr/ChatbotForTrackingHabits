import uvicorn
import asyncio
import bot.handlers
from utils.set_bot_commands import set_default_commands
from loader import bot


async def start():
    await set_default_commands(bot)
    await bot.polling()

if __name__ == '__main__':
    asyncio.run(start())
    # uvicorn.run('loader:app', reload=True)
    # set_default_commands(bot)
    # bot.infinity_polling()
    # uvicorn.run('loader:app', reload=True)
