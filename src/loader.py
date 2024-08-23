from telebot.async_telebot import AsyncTeleBot, StateMemoryStorage
from fastapi import FastAPI
from config import settings
from src.fast_api.routes import (
    registration_user,
    get_info_user,
    lifespan,
    login_user,
    create_habit,
    get_habit,
    get_list_habits,
    update_habit,
    delete_habit,
    set_reminder,
)

storage = StateMemoryStorage()
bot = AsyncTeleBot(token=settings.BOT_TOKEN, state_storage=storage)
app = FastAPI(
    title="Habit tracking",
    description="Api for tracking habits",
    lifespan=lifespan.lifespan
)

app.include_router(get_info_user.router)
app.include_router(login_user.router)
app.include_router(registration_user.router)
app.include_router(create_habit.router)
app.include_router(get_habit.router)
app.include_router(get_list_habits.router)
app.include_router(update_habit.router)
app.include_router(delete_habit.router)
app.include_router(set_reminder.router)
