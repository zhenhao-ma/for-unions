from app.crud.base import CRUDBase
from app import schemas
from pymongo import MongoClient
from .util import MaybeObjectId, ensure_object_id

class CRUDConnect(CRUDBase[schemas.Connect.DB]):

    def get_connect(self, m: MongoClient, *,  from_user: MaybeObjectId, to_user: MaybeObjectId):
        from_user = ensure_object_id(from_user)
        to_user = ensure_object_id(to_user)
        return self.first(m, query=schemas.QueryBase(
            filters={
                "$or": [
                    {"from_user": from_user, "to_user": to_user},
                    { "to_user": from_user, "from_user": to_user}
                ]
            }
        ))


connect = CRUDConnect(schemas.Connect.DB, collection_name="connect")
