from sqlalchemy.util import await_only
from telebot.async_telebot import AsyncTeleBot, StateMemoryStorage
from fastapi import FastAPI
from config import settings
from apscheduler.schedulers.asyncio import AsyncIOScheduler
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
    performing_habit,
)


scheduler: AsyncIOScheduler = AsyncIOScheduler()  # фоновый планировщик задач
storage: StateMemoryStorage = StateMemoryStorage()
bot: AsyncTeleBot = AsyncTeleBot(token=settings.BOT_TOKEN, state_storage=storage, parse_mode='html')
app: FastAPI = FastAPI(
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
app.include_router(performing_habit.router)
