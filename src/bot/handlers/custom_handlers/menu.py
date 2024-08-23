from telebot.types import Message
from src.loader import bot
from src.bot.keyboards import button_menu
from src.bot.utils_bot.get_user_jwt import get_header


@bot.message_handler(commands=['menu'])
async def menu(message: Message):
    header = await get_header(message.from_user.id)
    if header:
        await bot.send_message(message.chat.id, 'Выберите действие', reply_markup=button_menu.menu_button())
