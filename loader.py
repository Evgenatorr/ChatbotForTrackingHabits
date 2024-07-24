from telebot.async_telebot import AsyncTeleBot, StateMemoryStorage
from fastapi import FastAPI
from config import settings
from src.fast_api.routes import registration_user, get_info_user, lifespan, login_user

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
