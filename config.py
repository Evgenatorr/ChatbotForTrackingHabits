import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import BaseModel
from pathlib import Path
from fastapi.security import HTTPBearer

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    print('Переменные окружения загружены')

else:
    exit("Переменные окружения не загружены т.к отсутствует файл .env")

BASE_DIR = Path(__file__).parent


class SqliteDbConfig(BaseModel):
    _db_name: str = os.getenv('LITE_DB_NAME')
    _dialect_db: str = os.getenv('DIALECT_LITE_DB')
    _driver_db: str = os.getenv('DRIVER_LITE_DB')
    _path_lite_db: str = os.getenv('PATH_LITE_DB')

    url_db_sqlite: str = f"{_dialect_db}+{_driver_db}://{_path_lite_db}/{_db_name}"


class PostgresDbConfig(BaseModel):
    _db_name: str = os.getenv('DB_NAME')
    _dialect_db: str = os.getenv('DIALECT_DB')
    _driver_db: str = os.getenv('DRIVER_DB')
    _user_name_db: str = os.getenv('USER_NAME_DB')
    _user_pass_db: str = os.getenv('USER_PASS_DB')
    _host_db: str = os.getenv('HOST_DB')

    url_db_asyncpg: str = f"{_dialect_db}+{_driver_db}://{_user_name_db}:{_user_pass_db}@{_host_db}/{_db_name}"


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15


class Bot(BaseModel):
    default_commands: tuple = (
        ("start", "Старт"),
        ("help", "Вывести справку"),
        ("info", 'О себе')
    )


class Settings(BaseSettings):
    """
    Base settings for programm.
    """
    BASE_HOST: str = 'localhost'
    BASE_PORT: str = '8000'
    BASE_URL: str = f'http://{BASE_HOST}:{BASE_PORT}'
    BOT_TOKEN: str = os.getenv('BOT_TOKEN')
    BASE_DIR: str = os.path.dirname(__name__)
    TG_ADMIN_ID: str = os.getenv('TG_ADMIN_ID')
    api_v1_prefix: str = "/api/v1"
    security: HTTPBearer = HTTPBearer()
    auth_jwt: AuthJWT = AuthJWT()
    bot: Bot = Bot()
    db: PostgresDbConfig = PostgresDbConfig()
    lite_db: SqliteDbConfig = SqliteDbConfig()


settings = Settings()
