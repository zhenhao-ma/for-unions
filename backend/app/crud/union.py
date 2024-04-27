from app.crud.base import CRUDBase
from app import schemas
from pymongo import MongoClient


class CRUDUnion(CRUDBase[schemas.Union.DB]):

    def is_admin(self, m: MongoClient, *, user_id: schemas.ObjectId, union_id: schemas.ObjectId):
        return self.first(m, query=schemas.QueryBase(filters={
            "admins": user_id,
            "_id": union_id
        }))

union = CRUDUnion(schemas.Union.DB, collection_name="union")
