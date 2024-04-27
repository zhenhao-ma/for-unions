from typing import Generic, List, Optional, Type, TypeVar
from pydantic import BaseModel
from app.core.config import settings
from app.schemas.base import QueryBase
from pymongo import MongoClient
from pymongo.results import InsertOneResult
from pymongo.results import UpdateResult
from .util import cleanse_query_for_first, cleanse_query_for_list, MaybeObjectId, build_object_id, ensure_object_id

ModelType = TypeVar("ModelType", bound=BaseModel)


class CRUDBase(Generic[ModelType]):

    def __init__(self, model: Type[ModelType], collection_name: str, *, searchable: Optional[List[str]] = None):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD), and mongodb aggregation

        **Parameters**
        * `model`: A SQLAlchemy model class
        """
        self.model = model
        self.collection_name = collection_name
        self.searchable = searchable

    def first(self, m: MongoClient, query: Optional[QueryBase] = None) -> Optional[ModelType]:
        doc: dict = m[settings.MONGO_DB_DATABASE][self.collection_name].find_one({**cleanse_query_for_first(query, searchable_fields=self.searchable), "deleted": False})
        return self.model(**doc) if doc is not None else None

    def get_multi(
            self, m: MongoClient, *, query: QueryBase
    ) -> List[ModelType]:
        assert query.skip is not None and query.limit is not None, 'skip and limit is require for listing query'
        assert query.limit <= 50, 'limit is out of range'
        docs: List[dict] = list(m[settings.MONGO_DB_DATABASE][self.collection_name].find(
            {**cleanse_query_for_list(query, searchable_fields=self.searchable), "deleted": False}).skip(query.skip).limit(query.limit))
        return [self.model(**doc) for doc in docs]

    def create(self, m: MongoClient, *, obj_in: ModelType) -> InsertOneResult:
        return m[settings.MONGO_DB_DATABASE][self.collection_name].insert_one(obj_in.model_dump())

    def update(
            self, m: MongoClient, *, id: MaybeObjectId, obj_in: dict,
    ) -> UpdateResult:
        print("id : ", id)
        return m[settings.MONGO_DB_DATABASE][self.collection_name].update_one({'_id': build_object_id(id)},
                                                                              {'$set': obj_in})

    def hide(
            self, m: MongoClient, *, id: MaybeObjectId,
    ) -> UpdateResult:
        return self.update(m, id=id, obj_in={ "update": True })

    def first_by_id(self, m: MongoClient, *, id: MaybeObjectId):
        return self.first(m, query=QueryBase(id=id if isinstance(id, str) else str(id))) # convert type for inserted_id
