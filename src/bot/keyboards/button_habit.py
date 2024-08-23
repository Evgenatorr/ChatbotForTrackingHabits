from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def habit_button(header) -> ReplyKeyboardMarkup:

    button = ReplyKeyboardMarkup(row_width=1)

    button.add(
        KeyboardButton('Выполнить привычку'),
        KeyboardButton('Изменить описание привычки'),
        KeyboardButton('Удалить привычку')
    )
    return button