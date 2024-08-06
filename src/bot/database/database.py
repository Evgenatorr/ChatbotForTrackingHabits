from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings


engine: AsyncEngine = create_async_engine(settings.lite_db.url_db_sqlite, echo=False)
AsyncSession = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
async_session: AsyncSession = AsyncSession()

Base = declarative_base()


def init_db() -> None:
    """Инициализируем БД"""
    Base.metadata.create_all(engine)
