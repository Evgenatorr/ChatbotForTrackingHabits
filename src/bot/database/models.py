from sqlalchemy import (
    Column,
    Integer,
    String,
)
from src.bot.database.database import Base


class Token(Base):
    """
    Модель списка токенов
    """

    __tablename__: str = 'tokens'

    id: Column[int] = Column(Integer, primary_key=True)
    access_token: Column[str] = Column(String, nullable=False)
    token_type: Column[str] = Column(String, nullable=False)
    user_id: Column[int] = Column(Integer, nullable=False)
