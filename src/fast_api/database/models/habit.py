from src.fast_api.database.database import Base
from sqlalchemy import Column, ForeignKey, select, Time, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER, BIGINT
from sqlalchemy.ext.asyncio import AsyncSession


class Habit(Base):
    __tablename__ = "habit"

    id: Column[INTEGER] = Column(INTEGER, primary_key=True)
    user_id: Column[INTEGER] = Column(BIGINT, ForeignKey('user.tg_user_id', ondelete='CASCADE'), nullable=False)
    title: Column[VARCHAR] = Column(VARCHAR(50), nullable=False)
    description: Column[VARCHAR] = Column(VARCHAR(300))

    user = relationship(argument='User', back_populates="habits")
    tracking_habit = relationship(argument='HabitTracking', back_populates="habit",
                                  lazy='selectin',
                                  cascade="all, delete-orphan"
                                  )

    @classmethod
    async def get_habit_by_title(cls, title: str, tg_user_id: int, db: AsyncSession):
        habit = await db.execute(
            select(cls).where(
                cls.title.ilike(title), cls.user_id == tg_user_id
            )
        )

        return habit.scalar()

    @classmethod
    async def get_habit_by_id(cls, habit_id: int, tg_user_id: int, db: AsyncSession):
        habit = await db.execute(
            select(cls).where(
                cls.id == habit_id, cls.user_id == tg_user_id
            )
        )
        return habit.scalar()


class HabitTracking(Base):
    __tablename__ = "habit_tracking"

    id: Column[INTEGER] = Column(INTEGER, primary_key=True)
    habit_id: Column[INTEGER] = Column(INTEGER, ForeignKey('habit.id', ondelete='CASCADE'), nullable=False)
    alert_time: Column[DateTime] = Column(DateTime(timezone=True))
    count: Column[INTEGER] = Column(INTEGER, default=0)

    habit = relationship(argument='Habit', back_populates="tracking_habit", lazy='selectin')

    @classmethod
    async def get_habit_tracking_by_id(cls, habit_id: int, tg_user_id: int, db: AsyncSession):
        habit = await db.execute(
            select(cls).where(
                cls.habit_id == habit_id, cls.habit == tg_user_id
            )
        )
        return habit.scalar()