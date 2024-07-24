from loader import bot


@bot.message_handler(content_types=['text'])
async def echo_all(message):
    await bot.reply_to(message, message.text)
