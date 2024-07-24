"""
Модуль добавление кнопки логин
"""

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def login_button() -> InlineKeyboardMarkup:
    """
    Функция в которой добавляются кнопки 'Вход', 'Регистрация'
    :return: button
    """

    button = InlineKeyboardMarkup(row_width=1)
    button.add(
        InlineKeyboardButton('Вход', callback_data='login'),
        InlineKeyboardButton('Регистрация', callback_data='registration')
    )

    return button
