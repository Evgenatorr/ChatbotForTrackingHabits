from datetime import timedelta
import datetime
import bcrypt
import jwt
from config import settings


def encode_jwt(
        payload: dict,
        private_key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None,
) -> str:
    """
    Функция кодирования токена
    """

    to_encode: dict = payload.copy()
    now: datetime.datetime = datetime.datetime.now(datetime.UTC)

    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )

    encoded: str = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )

    return encoded


def decode_jwt(
        token: str | bytes,
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
) -> dict:
    """
    Функция декодирования токена
    """

    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded


def hash_password(
        password: str,
) -> bytes:
    """
    Функция для хеширования пароля
    """

    salt: bytes = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(
        password: str,
        hashed_password: bytes,
) -> bool:
    """
    Функция для проверки хэшированного пароля
    """

    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )
