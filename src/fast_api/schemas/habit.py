from pydantic import BaseModel, ConfigDict, Field, AwareDatetime
from datetime import time
from typing import Optional


class BaseHabitSchema(BaseModel):

    title: str = Field(description='Title habit')
    description: str = Field(description='Description habit')


class HabitUpdateSchema(BaseModel):

    title: Optional[str] = None
    description: Optional[str] = None



class HabitTrackingSchema(BaseModel):

    habit_id: int = Field(description='Habit id')
    alert_time: AwareDatetime | None = Field(description='Habit alert time')
    count: int = Field(description='Habit completion days counter')

class HabitPublicSchema(BaseHabitSchema):
    id: int = Field(description='Habit id in db')
    user_id: int = Field(description='User id in telegram')
    tracking_habit: list[HabitTrackingSchema]

class SetReminderSchema(BaseModel):

    alert_time: str | AwareDatetime | None = Field(description='Habit alert time')
