from sqlalchemy import (
    Column,
    Integer,
    String,
    select,
)

from src.bot.database.database import Base, async_session


class Token(Base):
    """
    Модель списка токенов
    """

    __tablename__: str = 'tokens'

    id: Column[int] = Column(Integer, primary_key=True)
    access_token: Column[str] = Column(String, nullable=False)
    token_type: Column[str] = Column(String, nullable=False)
    user_tg_id: Column[int] = Column(Integer, nullable=False)

    @classmethod
    async def get_token_by_user_id(cls, user_tg_id: int):
        """
        Функция для получения токена по tg id user из таблицы sqlite на стороне бота
        """

        token = await async_session.execute(select(cls).where(user_tg_id == cls.user_tg_id))
        return token.scalar()
