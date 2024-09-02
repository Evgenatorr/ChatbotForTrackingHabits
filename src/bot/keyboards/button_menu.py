from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def menu_button() -> InlineKeyboardMarkup:
    """
    Функция в которой добавляются кнопки в главное меню
    :return: button
    """

    button: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    button.add(
        InlineKeyboardButton('Привычки', callback_data='list_habit'),
        InlineKeyboardButton('Добавить привычку', callback_data='create_habit'),
    )

    return button


def add_habit_button() -> InlineKeyboardMarkup:
    """
    Функция в которой добавляются кнопку 'Добавить привычку'
    :return: button
    """

    button: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    button.add(
        InlineKeyboardButton('Добавить привычку', callback_data='create_habit'),
    )

    return button
