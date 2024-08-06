from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from typing import AsyncGenerator
from config import settings


engine = create_async_engine(settings.db.url_db_asyncpg)
Base = declarative_base()
async_session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session.begin() as session:
        try:
            yield session
        except:
            await session.rollback()
            raise
        finally:
            await session.close()


# async def init_db():
#     """Инициализируем БД"""
#     await Base.metadata.create_all(engine)
