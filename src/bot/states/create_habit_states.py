from telebot.asyncio_handler_backends import State, StatesGroup


class CreateHabitState(StatesGroup):
    add_title = State()
    add_description = State()
