from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker, declarative_base

from config import settings

engine: AsyncEngine = create_async_engine(settings.db.url_db_asyncpg)
Base = declarative_base()
AsyncSession: sessionmaker = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
async_session: AsyncSession = AsyncSession()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession.begin() as session:
        try:
            yield session
        except:
            await session.rollback()
            raise
        finally:
            await session.close()
