from src.fast_api.database.database import Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER, BOOLEAN, DATE, BYTEA, TIMESTAMP


class User(Base):
    __tablename__ = "user"

    id: Column[INTEGER] = Column(INTEGER, primary_key=True)
    tg_user_id: Column[INTEGER] = Column(INTEGER, nullable=False, unique=True)
    username: Column[VARCHAR] = Column(VARCHAR(50), nullable=False)
    password: Column[VARCHAR] = Column(BYTEA, nullable=False)
    role: Column[VARCHAR] = Column(VARCHAR(20), nullable=False)
    active: Column[BOOLEAN] = Column(BOOLEAN, default=True)

    habits = relationship(argument='Habit', back_populates='user')


class Habit(Base):
    __tablename__ = "habit"

    id: Column[INTEGER] = Column(INTEGER, primary_key=True)
    user_id: Column[INTEGER] = Column(INTEGER, ForeignKey('user.id'), nullable=False)
    title: Column[VARCHAR] = Column(VARCHAR(50), nullable=False)
    description: Column[VARCHAR] = Column(VARCHAR(300))

    user = relationship(argument='User', back_populates="habits")
    tracking_habit = relationship(argument='HabitTracking', back_populates="habit")


class HabitTracking(Base):
    __tablename__ = "habit_tracking"

    id: Column[INTEGER] = Column(INTEGER, primary_key=True)
    habit_id: Column[INTEGER] = Column(INTEGER, ForeignKey('user.id'), nullable=False)
    alert_time: Column[TIMESTAMP] = Column(TIMESTAMP(timezone=True), nullable=False)
    count: Column[INTEGER] = Column(INTEGER, default=0)

    habit = relationship(argument='Habit', back_populates="tracking_habit")
