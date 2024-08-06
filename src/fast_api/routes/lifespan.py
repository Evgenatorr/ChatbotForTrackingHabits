import contextlib
from src.fast_api.database.database import engine, Base


@contextlib.asynccontextmanager
async def lifespan(app):
    yield

