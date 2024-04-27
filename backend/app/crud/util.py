from app.schemas.base import QueryBase
from bson import ObjectId
from typing import Optional, List, Union
from app.helpers import is_pydantic_field_empty
import re


def cleanse_query_for_first(query: Optional[QueryBase], *, searchable_fields: Optional[List[str]] = None) -> dict:
    if query is None: return {}
    base = query.filters if query.filters is not None else {}
    base = __build_id_query(base, query)
    base = __build_searchable_query(base, searchable_fields, query)
    return base


def cleanse_query_for_list(query: QueryBase, *, searchable_fields: Optional[List[str]] = None) -> dict:
    base = query.filters if query.filters is not None else {}
    base = __build_ids_query(base, query)
    base = __build_searchable_query(base, searchable_fields, query)
    return base

MaybeObjectId = Union[str, ObjectId]



def build_object_id(id: Union[MaybeObjectId, List[MaybeObjectId]]) -> Union[ObjectId, List[ObjectId]]:
    if isinstance(id, list): return [build_object_id(i) for i in id]
    if isinstance(id, str): return ObjectId(id)
    return id

def __build_id_query(base_query: dict, query: QueryBase) -> dict:
    if is_pydantic_field_empty(query, 'id'): return base_query
    # use $and if necessary
    q = { '_id': build_object_id(query.id) }
    return { '$and': [base_query, q] } if '_id' in base_query else { **base_query, **q }

def __build_ids_query(base_query: dict, query: QueryBase) -> dict:
    if is_pydantic_field_empty(query, 'ids'): return base_query
    # use $and if necessary
    q = { '_id': {  '$in': build_object_id(query.ids) } }
    return { '$and': [base_query, q] } if '_id' in base_query else { **base_query, **q }

def __build_searchable_query(base_query: dict, searchable_fields: Optional[List[str]], query: QueryBase) -> dict:
    if searchable_fields is None or len(searchable_fields) == 0 or is_pydantic_field_empty(query, 'search'): return base_query
    # Note also that regex's anchored at the start (ie: starting with ^) are able to use indexes in the db,
    # and will run much faster in that case. –
    regx = re.compile(query.search, re.IGNORECASE)
    _or_logics: List[dict] = []
    for f in searchable_fields:
        _or_logics.append({f: regx})
    # reduce the query
    _or: dict = _or_logics[0] if len(_or_logics) == 1 else { '$or': _or_logics }
    # use $and if necessary
    return {'$and': [base_query,_or]} if '$or' in base_query else { **base_query, **_or }

def ensure_object_id(id: MaybeObjectId) -> ObjectId:
    if isinstance(id, str): return ObjectId(id)
    return id