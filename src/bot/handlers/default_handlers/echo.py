from src.loader import bot


@bot.message_handler(func=lambda message: True)
async def echo_all(message):
    await bot.reply_to(message, message.text)