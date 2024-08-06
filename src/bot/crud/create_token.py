from src.bot.database.database import async_session
from src.bot.database import models
from src.bot import schemas


async def create_token(token: schemas.token.CreateToken):
    """Добавить токен в бд."""

    token_in_db = await models.Token.get_token_by_user_id(token.user_tg_id)
    if token_in_db is None:
        token = models.Token(
            **token.model_dump()
        )

        async_session.add(token)
        await async_session.commit()
        # await async_session.refresh(token)

    else:
        token_in_db.access_token = token.access_token
        await async_session.commit()
