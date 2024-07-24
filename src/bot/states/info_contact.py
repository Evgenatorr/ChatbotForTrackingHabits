"""
Модуль хранения состояний пользователя
"""
from telebot.asyncio_handler_backends import State, StatesGroup


class UserState(StatesGroup):
    registration = State()
    login = State()
    main = State()
    create_habit = State()
    delete_habit = State()
    get_all_habits = State()
    get_habit = State()
    set_reminder_habit = State()
    update_habit = State()
