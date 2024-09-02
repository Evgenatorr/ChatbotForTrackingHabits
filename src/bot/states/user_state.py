from telebot.asyncio_handler_backends import State, StatesGroup


class UserState(StatesGroup):
    registration = State()
    login = State()
