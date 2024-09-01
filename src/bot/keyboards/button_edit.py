"""
Модуль добавление кнопки редактирование привычки
"""

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def edit_button() -> InlineKeyboardMarkup:
    """
    Функция в которой добавляются кнопки выбора действия с привычкой
    :return: button
    """

    button = InlineKeyboardMarkup(row_width=1)
    button.add(
        InlineKeyboardButton('О привычке', callback_data='info_habit'),
        InlineKeyboardButton('Выполнить привычку', callback_data='performing_habit'),
        InlineKeyboardButton('Изменить привычку', callback_data='edit_habit'),
        InlineKeyboardButton('Установить | Изменить напоминание', callback_data='set_reminder'),
        InlineKeyboardButton('Удалить напоминание', callback_data='delete_reminder'),
        InlineKeyboardButton('Удалить привычку', callback_data='delete_habit'),
        InlineKeyboardButton(text='Меню', callback_data=f'back_to_menu')
    )

    return button

def choice_edit_habit() -> InlineKeyboardMarkup:
    """
    Функция в которой добавляются кнопки выбора, что изменить в привычке
    :return: button
    """

    button = InlineKeyboardMarkup(row_width=1)
    button.add(
        InlineKeyboardButton('Описание', callback_data='edit_description'),
        InlineKeyboardButton('Название', callback_data='edit_title'),
        # InlineKeyboardButton('Название и описание', callback_data='edit_title_and_description'),
    )

    return button


