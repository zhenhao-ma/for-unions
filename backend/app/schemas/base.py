from datetime import datetime
from typing import Any, Optional, Tuple, Type, TypeVar, List, Union, Annotated, get_origin, get_args

from pydantic import BaseModel, create_model, Field, GetJsonSchemaHandler, AliasChoices
from pydantic.fields import FieldInfo
from copy import deepcopy
from pydantic_core import core_schema
from bson import ObjectId as _ObjectId
from pydantic.json_schema import JsonSchemaValue


def is_optional(field):
    return get_origin(field) is Union and \
           type(None) in get_args(field)


class ObjectIdPydanticAnnotation:
    @classmethod
    def validate_object_id(cls, v: Any, handler) -> _ObjectId:
        if isinstance(v, _ObjectId):
            return v

        s = handler(v)
        if _ObjectId.is_valid(s):
            return _ObjectId(s)
        else:
            raise ValueError("Invalid ObjectId")

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, _handler) -> core_schema.CoreSchema:
        assert source_type is _ObjectId or (is_optional(source_type) and _ObjectId in get_args(source_type))
        return core_schema.no_info_wrap_validator_function(
            cls.validate_object_id,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema, handler) -> JsonSchemaValue:
        return handler(core_schema.str_schema())


ObjectId = Annotated[_ObjectId, ObjectIdPydanticAnnotation]


class SchemaBase(BaseModel):
    created: datetime = Field(default_factory=datetime.utcnow)
    updated: datetime = Field(default_factory=datetime.utcnow)
    deleted: bool = False


class DbBase(BaseModel):
    id: ObjectId = Field(..., alias=AliasChoices('_id', 'id'))


class QueryBase(BaseModel):
    skip: Optional[int] = None
    limit: Optional[int] = None
    search: Optional[str] = None
    id: Optional[Union[ObjectId, str]] = None
    ids: Optional[List[Union[ObjectId, str]]] = None
    filters: Optional[dict] = None

    @classmethod
    def loop(cls, func, *args, **kwargs) -> List[Any]:
        page = 0
        page_size = 50
        res = []
        has_more = True
        base_query: QueryBase = kwargs.get("query")
        if 'query' in kwargs: del kwargs['query']
        base_query_dict: dict = base_query.model_dump() if base_query is not None else {}
        if 'skip' in base_query_dict: del base_query_dict['skip']
        if 'limit' in base_query_dict: del base_query_dict['limit']
        while page < 10000 and has_more:
            query = QueryBase(**base_query_dict, limit=page_size, skip=page * page_size)
            output = func(*args, **kwargs, query=query)
            if len(output) == 0: break
            has_more = len(output) == page_size
            res += output
            page += 1
        return res


"""Util functions to make optional cls"""


def make_field_optional(field: FieldInfo, default: Any = None) -> Tuple[Any, FieldInfo]:
    new = deepcopy(field)
    new.default = default
    new.annotation = Optional[field.annotation]  # type: ignore
    return (new.annotation, new)


BaseModelT = TypeVar('BaseModelT', bound=SchemaBase)


def make_partial_model(model: Type[BaseModelT]) -> Type[BaseModelT]:
    return create_model(  # type: ignore
        f'Optional{model.__name__}',
        __base__=model,
        __module__=model.__module__,
        **{
            field_name: make_field_optional(field_info)
            for field_name, field_info in model.model_fields.items()
        })
