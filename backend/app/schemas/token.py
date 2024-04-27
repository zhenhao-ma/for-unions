from pydantic import BaseModel, Field
from .user import User

class Token(BaseModel):
    access_token: str = Field(None)
    token_type: str = Field(default='bearer')
    user: User.ResDetailed


class TokenPayloadSub(BaseModel):
    user_id: str


class TokenPayload(BaseModel):
    sub: str
