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
        InlineKeyboardButton('Изменить привычку', callback_data='update_habit'),
        InlineKeyboardButton('Выполнить привычку', callback_data='habit_fixation'),
        InlineKeyboardButton('Статистика привычек', callback_data='statistics_habit'),
        InlineKeyboardButton('Установить напоминание', callback_data='set_reminder'),
    )

    return button
