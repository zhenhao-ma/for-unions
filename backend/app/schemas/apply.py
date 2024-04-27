from datetime import datetime
from typing import Optional, List

from pydantic import Field, EmailStr
from .base import ObjectId, DbBase
from app.schemas.base import SchemaBase, make_partial_model
from app.helpers import enum


class Apply:
    class Apply(SchemaBase):
        union: ObjectId
        description: Optional[str] = None

    class Review(SchemaBase):
        apply_id: ObjectId
        status: enum.ReviewStatus
        rejected_reason: Optional[str] = None

    class _Res(SchemaBase):
        union: ObjectId
        union_name: Optional[str] = None
        applicant: ObjectId
        applicant_name: Optional[str] = None
        applicant_phone: Optional[str] = None
        status: enum.ReviewStatus
        handler: Optional[ObjectId] = None
        description: Optional[str] = None
        rejected_reason: Optional[str] = None

    class Base(_Res): ...

    Optional = make_partial_model(Base)

    class DB(Base, DbBase): ...

    class Res(_Res, DbBase): ...