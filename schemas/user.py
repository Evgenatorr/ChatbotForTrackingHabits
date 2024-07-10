from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    name: str
    surname: str
    hashed_password: bytes
    role: str
