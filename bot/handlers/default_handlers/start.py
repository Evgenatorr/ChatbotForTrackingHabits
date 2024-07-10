from loader import bot
import requests
from config import settings


@bot.message_handler(commands=['start'], state=None)
async def send_welcome(message):
    response = requests.get(settings.BASE_URL)
    await bot.reply_to(message, response.text)
