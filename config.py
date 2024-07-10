import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import BaseModel
from pathlib import Path


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    print('Переменные окружения загружены')

else:
    exit("Переменные окружения не загружены т.к отсутствует файл .env")

BASE_DIR = Path(__file__).parent


class DbConfig(BaseModel):
    db_name: str = os.getenv('DB_NAME')
    dialect_db: str = os.getenv('DIALECT_DB')
    driver_db: str = os.getenv('DRIVER_DB')
    user_name_db: str = os.getenv('USER_NAME_DB')
    pass_db: str = os.getenv('PASS_DB')
    host_db: str = os.getenv('HOST_DB')

    url_db: str = f"{dialect_db}+{driver_db}://{user_name_db}:{pass_db}@{host_db}/{db_name}"


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15


class Bot(BaseModel):
    default_commands: tuple = (
        ("start", "Регистрация/Старт"),
        ("help", "Вывести справку")
    )


class Settings(BaseSettings):
    """
    Base settings for programm.
    """
    BASE_HOST: str = 'localhost'
    BASE_PORT: str = '8000'
    BASE_URL: str = f'http://{BASE_HOST}:{BASE_PORT}/'
    BOT_TOKEN: str = os.getenv('BOT_TOKEN')
    BASE_DIR: str = os.path.dirname(__name__)

    auth_jwt: AuthJWT = AuthJWT()
    bot: Bot = Bot()
    db: DbConfig = DbConfig()


settings = Settings()
