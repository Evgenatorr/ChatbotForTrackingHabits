from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def habit_button(habits) -> InlineKeyboardMarkup:
    """
    Функция добавляет кнопки выбора привычки
    """

    button: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    button.add(
        *[InlineKeyboardButton(text=habit_name, callback_data=f'title_{habit_name}') for habit_name in habits],
        InlineKeyboardButton(text='🔙', callback_data=f'back_to_menu')
    )

    return button
