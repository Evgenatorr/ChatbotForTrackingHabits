from pydantic import BaseModel, ConfigDict, Field


class BaseUserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str = Field(description='Login in telegram')
    tg_user_id: int = Field(description='User id in telegram')
    role: str = Field(description='Role in telegram')
    active: bool = Field(description='Active or inactive', default=True)


class CreateUserSchema(BaseUserSchema):
    model_config = ConfigDict(strict=True)

    password: str = Field(description='Password in telegram')

class UserOutSchema(CreateUserSchema):
    password: bytes = Field(description='Password in telegram')
