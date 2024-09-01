from telebot.asyncio_handler_backends import State, StatesGroup


class EditHabitState(StatesGroup):
    edite = State()
    save_description = State()
    save_title = State()
    save_description_and_title = State()
    save_reminder_time = State()
