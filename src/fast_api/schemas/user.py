from pydantic import BaseModel, ConfigDict, Field


class CreateUser(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str = Field(description='Login in telegram')
    tg_user_id: int = Field(description='User id in telegram')
    password: str = Field(description='Password in telegram')
    role: str = Field(description='Role in telegram')
    active: bool = Field(description='Active or inactive', default=True)


class UserOut(CreateUser):
    password: bytes = Field(description='Password in telegram')
