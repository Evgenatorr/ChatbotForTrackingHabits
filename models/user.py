from database.database import Base
from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER
# from habit import Habit


class User(Base):
    __tablename__ = "users"

    id: Column[INTEGER] = Column(INTEGER, primary_key=True)
    name: Column[VARCHAR] = Column(VARCHAR(50), nullable=False)
    surname: Column[VARCHAR] = Column(VARCHAR(50), nullable=False)
    # hashed_password: Column[VARCHAR] = Column(VARCHAR(100), nullable=False)
    role: Column[VARCHAR] = Column(VARCHAR(20), nullable=False)

    # habits = relationship(argument='Habit', backref='habits')
