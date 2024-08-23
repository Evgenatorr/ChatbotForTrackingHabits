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
        InlineKeyboardButton('О себе', callback_data='info'),
        InlineKeyboardButton('Список привычек', callback_data='list_habit'),
        InlineKeyboardButton('Редактировать привычку', callback_data='habit_edit'),
        InlineKeyboardButton('Статистика привычек', callback_data='statistics_habit'),
        InlineKeyboardButton('Установить напоминание', callback_data='set_reminder'),
        InlineKeyboardButton('Добавить привычку', callback_data='create_habit'),
    )

    return button
