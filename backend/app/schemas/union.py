from datetime import datetime
from typing import Optional, List

from pydantic import Field, EmailStr
from .base import ObjectId, DbBase
from app.schemas.base import SchemaBase, make_partial_model
from app.helpers import enum


class Union:
    class Create(SchemaBase):
        phone: str = ""
        email: str = ""
        name: str
        description: str = ""

    class Update(SchemaBase):
        phone: str = ""
        email: str = ""
        name: str = ""
        description: str = ""

    class _Res(SchemaBase):
        phone: str
        email: str
        admins: List[ObjectId]
        name: str
        description: str = ""
        logo: Optional[ObjectId] = None

    class Base(_Res): ...

    Optional = make_partial_model(Base)

    class DB(Base, DbBase):...
    class Res(_Res, DbBase):...