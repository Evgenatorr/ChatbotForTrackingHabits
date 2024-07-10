from database.database import Base
from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER, BOOLEAN, DATE
# from user import User


class Habit(Base):
    __tablename__ = "habits"

    id: Column[INTEGER] = Column(INTEGER, primary_key=True)
    # user_id: Column[INTEGER] = Column(INTEGER, ForeignKey="users.id", nullable=False)
    title: Column[VARCHAR] = Column(VARCHAR(50), nullable=False)
    description: Column[VARCHAR] = Column(VARCHAR(300))
    amount_days: Column[INTEGER] = Column(INTEGER, default=21)
    # done: Column[BOOLEAN] = Column(BOOLEAN)
    start_date: Column[DATE] = Column(DATE)

    # user = relationship(argument='User', backref="users")
