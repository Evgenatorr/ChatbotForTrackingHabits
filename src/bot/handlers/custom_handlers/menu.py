from telebot.types import Message
from src.loader import bot
from src.bot.keyboards import button_menu
from src.bot.utils_bot.get_user_jwt import get_user
from src.bot.states.user_state import UserState


@bot.message_handler(commands=['menu'])
async def menu(message: Message):
    user = await get_user(message.from_user.id)
    if user:
        # bot.set_state(message.from_user.id, state=UserState.menu)
        await bot.send_message(message.chat.id, 'Выберите действие', reply_markup=button_menu.menu_button())
