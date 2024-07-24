from pydantic import BaseModel, Field


class TokenInfo(BaseModel):
    access_token: str = Field(description='JSON Web Token')
    token_type: str = Field(description='Type JSON Web Token')


class CreateToken(TokenInfo):
    user_id: int = Field(description='Telegram user id')
