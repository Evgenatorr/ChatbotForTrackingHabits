from telebot.types import Message, CallbackQuery
from src.loader import bot
from src.bot.keyboards import button_menu
from src.bot.utils_bot.get_user_jwt import get_header


@bot.message_handler(commands=['menu'])
async def menu(message: Message):
    header = await get_header(message.from_user.id)

    if header:
        try:
            await bot.edit_message_text(chat_id=message.chat.id,
                                        message_id=message.id,
                                        text='<strong>Меню</strong>',
                                        reply_markup=button_menu.menu_button())

        except Exception as exc:
            print(exc)
            await bot.send_message(chat_id=message.chat.id,
                                        text='<strong>Меню</strong>',
                                        reply_markup=button_menu.menu_button())


@bot.callback_query_handler(func=lambda call: call.data == 'back_to_menu')
async def menu(call: CallbackQuery):
    header = await get_header(call.from_user.id)

    if header:

        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.id,
                                    text='<strong>Меню</strong>',
                                    reply_markup=button_menu.menu_button())
