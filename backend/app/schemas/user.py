from datetime import datetime
from typing import Optional, List

from pydantic import Field, EmailStr, ConfigDict
from .base import ObjectId, DbBase
from app.schemas.base import SchemaBase, make_partial_model
from app.helpers import enum


class User:
    class ReqRegister(SchemaBase):
        phone: str
        email: str

    class Update(SchemaBase):
        full_name: Optional[str]
        country: Optional[enum.Country] = None
        tags: Optional[List[str]] = []
        avatar: Optional[str] = None
        description: Optional[str] = None
        connect_type: Optional[enum.ConnectType] = None

    class _ResPreview(SchemaBase):
        country: enum.Country = enum.Country.CN
        full_name: str = Field("", max_length=30)
        role: enum.Role = enum.Role.USER
        unions: List[ObjectId] = []
        tags: List[str] = []
        avatar: Optional[str] = None
        description: str = ""
        connect_type: enum.ConnectType = enum.ConnectType.REQUIRE_APPROVE

    class _ResDetailed(_ResPreview):
        phone: str
        email: Optional[EmailStr] = None

    class Base(_ResDetailed):
        openid: Optional[str] = None
        wechat_session_key: Optional[str] = None

    Optional = make_partial_model(Base)

    class DB(Base, DbBase): ...

    class ResPreview(_ResPreview, DbBase): ...

    class ResDetailed(_ResDetailed, DbBase): ...
