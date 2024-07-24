from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings


engine = create_async_engine(settings.lite_db.url_db_sqlite, echo=False)
AsyncSession = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
async_session = AsyncSession()

Base = declarative_base()


def init_db() -> None:
    """Инициализируем БД"""
    Base.metadata.create_all(engine)
