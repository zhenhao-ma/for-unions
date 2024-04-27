from datetime import datetime
from typing import Optional, List

from pydantic import Field, EmailStr
from .base import ObjectId, DbBase
from app.schemas.base import SchemaBase, make_partial_model
from app.helpers import enum


class Connect:
    class Create(SchemaBase):
        to_user: ObjectId
        description: Optional[str] = None

    class Review(SchemaBase):
        id: ObjectId
        status: enum.ReviewStatus

    class _Res(SchemaBase):
        from_user: ObjectId
        to_user: ObjectId
        status: enum.ReviewStatus
        description: Optional[str] = None

    class Base(_Res): ...

    Optional = make_partial_model(Base)

    class DB(Base, DbBase): ...

    class Res(_Res, DbBase): ...