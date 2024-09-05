from sqlalchemy.ext.asyncio import AsyncSession
from src.fast_api.database.database import Base
from sqlalchemy import Column, ForeignKey, select, Time
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER, BOOLEAN, BYTEA, BIGINT


class User(Base):
    __tablename__ = "user"

    id: Column[INTEGER] = Column(INTEGER, primary_key=True)
    tg_user_id: Column[INTEGER] = Column(BIGINT, nullable=False, unique=True)
    username: Column[VARCHAR] = Column(VARCHAR(50), nullable=False)
    password: Column[VARCHAR] = Column(BYTEA, nullable=False)
    active: Column[BOOLEAN] = Column(BOOLEAN, default=True)

    habits = relationship(argument='Habit', back_populates='user')

    @classmethod
    async def get_user_by_username_and_tg(cls, username: str, tg_user_id: int, db: AsyncSession):
        """
        Функция получения пользователя по логину(username)
        """

        user = await db.execute(
            select(cls).where(
                cls.username == username, cls.tg_user_id == tg_user_id
            )
        )

        return user.scalar()

    @classmethod
    async def get_user_by_tg_id(cls, tg_user_id: int, db: AsyncSession):
        """
        Функция получения пользователя по логину(username)
        """

        user = await db.execute(
            select(cls).where(
                cls.tg_user_id == tg_user_id
            )
        )

        return user.scalar()

    @classmethod
    async def get_user_by_username(cls, username: str, db: AsyncSession):
        """
        Функция получения пользователя по логину(username)
        """

        user = await db.execute(
            select(cls).where(
                cls.username == username
            )
        )

        return user.scalar()

