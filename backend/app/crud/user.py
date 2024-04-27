from app.crud.base import CRUDBase
from app import schemas
from app.helpers import enum
from pymongo import MongoClient


class CRUDUser(CRUDBase[schemas.User.DB]):

    def is_admin(self, user_db: schemas.User.DB):
        return user_db.role in [enum.Role.ADMIN, enum.Role.ROOT]

    def is_root(self, user_db: schemas.User.DB):
        return user_db.role == enum.Role.ROOT

    def first_by_email(self, m: MongoClient, *, email: str):
        return self.first(m, query=schemas.QueryBase(filters={
            "email": email
        }))

    def first_by_phone(self, m: MongoClient, *, phone: str):
        return self.first(m, query=schemas.QueryBase(filters={
            "phone": phone
        }))


user = CRUDUser(schemas.User.DB, collection_name="user")
