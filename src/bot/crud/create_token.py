from src.bot.database.database import async_session
from src.bot.database import models
from src.bot import schemas


async def create_token(data: schemas.token.CreateToken):
    """Добавить токен в бд."""
    user = models.Token(
        access_token=data['access_token'],
        token_type=data['token_type'],
        user_id=data['user_id']
    )
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)
