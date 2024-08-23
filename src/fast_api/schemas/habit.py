from pydantic import BaseModel, ConfigDict, Field
from datetime import time
from typing import Optional


class BaseHabitSchema(BaseModel):

    title: str = Field(description='Title habit')
    description: str = Field(description='Description habit')


class HabitUpdateSchema(BaseModel):

    title: str | None = None
    description: str | None = None


class HabitPublicSchema(BaseHabitSchema):
    id: int = Field(description='Habit id in db')
    user_id: int = Field(description='User id in telegram')


class HabitTrackingSchema(BaseModel):

    habit_id: int = Field(description='Habit id')
    alert_time: time = Field(description='Habit alert time')
    count: int = Field(description='Habit completion days counter')


class AddReminderSchema(BaseModel):

    alert_time: str = Field(description='Habit alert time')
