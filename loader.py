from telebot.async_telebot import AsyncTeleBot
from fastapi import FastAPI
from config import settings
from api.routes import router, lifespan


bot = AsyncTeleBot(token=settings.BOT_TOKEN)
app = FastAPI(
    title="Habit tracking",
    description="Api for tracking habits",
    lifespan=lifespan
)
app.include_router(router)
