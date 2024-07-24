"""
Модуль добавление кнопки инфо
"""

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def info_button() -> InlineKeyboardMarkup:
    """
    Функция в которой добавляются кнопки 'О себе'
    :return: button
    """

    button = InlineKeyboardMarkup(row_width=1)
    button.add(
        InlineKeyboardButton('О себе', callback_data='info'),
    )

    return button
