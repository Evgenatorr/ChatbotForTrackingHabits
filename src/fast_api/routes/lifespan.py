import contextlib
from src.fast_api.database.database import engine, Base


@contextlib.asynccontextmanager
async def lifespan(app):
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    #     await conn.run_sync(Base.metadata.create_all)
    yield
