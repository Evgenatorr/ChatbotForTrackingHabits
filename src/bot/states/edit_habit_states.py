from telebot.asyncio_handler_backends import State, StatesGroup


class EditHabitState(StatesGroup):
    title = State()

