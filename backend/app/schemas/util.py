from pydantic import BaseModel
from typing import Optional, Union


class Watermark(BaseModel):
    appid: str
    timestamp: float


class PhoneInfo(BaseModel):
    phoneNumber: str
    purePhoneNumber: str
    countryCode: Union[str, int, float]
    watermark: Watermark


class Wechat:
    class Code2SessionResponse(BaseModel):
        openid: str
        session_key: str
        unionid: Optional[str] = None

    class GetAccessTokenResponse(BaseModel):
        access_token: str
        expires_in: float
        errcode: Optional[int] = None
        errmsg: Optional[str] = None

    class GetPhoneNumberResponse(BaseModel):
        errcode: Optional[int] = None
        errmsg: Optional[str] = None
        phone_info: PhoneInfo

    class PhoneInfoPublic(BaseModel):
        phone: str
        secret: str


class Status(BaseModel):
    status: bool
