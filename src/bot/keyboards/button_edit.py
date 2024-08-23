"""
Модуль добавление кнопки редактирование привычки
"""

from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def edit_button() -> ReplyKeyboardMarkup:
    """
    Функция в которой добавляются кнопки 'Меню'
    :return: button
    """

    button = ReplyKeyboardMarkup(row_width=1)

    button.add(
        KeyboardButton('Выполнить привычку'),
        KeyboardButton('Изменить описание привычки'),
        KeyboardButton('Удалить привычку')
    )

    return button
