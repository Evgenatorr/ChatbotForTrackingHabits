"""
Модуль добавление кнопки инфо
"""

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def menu_button() -> InlineKeyboardMarkup:
    """
    Функция в которой добавляются кнопки 'Меню'
    :return: button
    """

    button = InlineKeyboardMarkup(row_width=1)
    button.add(
        InlineKeyboardButton('Привычки', callback_data='list_habit'),
        InlineKeyboardButton('Добавить привычку', callback_data='create_habit'),
    )

    return button
