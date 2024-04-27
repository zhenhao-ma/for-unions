from typing import Generator, Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from redis import Redis
from app.core import security
from pydantic import ValidationError
from jose import jwt
from app import db, schemas, crud

from app.core.config import settings
from pymongo import MongoClient

import json

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/users/public/access-token"
)
reusable_oauth2_close_auto_error = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/users/public/access-token",
    auto_error=False
)


def get_redis() -> Redis:
    yield db.get_redis()


def get_mongo() -> MongoClient:
    yield db.get_mongo()


def __get_user_by_token(m: MongoClient, *, token: str) -> schemas.User.DB:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        print('payload: ', payload)
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise ValueError("TokenExpired")

    payload_sub = schemas.TokenPayloadSub(**json.loads(token_data.sub))
    user = crud.user.first_by_id(m, id=payload_sub.user_id)

    if not user or user.deleted:
        raise ValueError("UserNotFound")
    return user


def get_current_user(
        m: MongoClient = Depends(get_mongo), token: str = Depends(reusable_oauth2)
) -> schemas.User.DB:
    return __get_user_by_token(m, token=token)


def get_optional_user(
        m: MongoClient = Depends(get_mongo), token: str = Depends(reusable_oauth2_close_auto_error)
) -> Optional[schemas.User.DB]:
    try:
        user = __get_user_by_token(m, token=token)
    except (AttributeError, ValueError):
        user = None
    return user


def get_current_admin(
        current_user: schemas.User.DB = Depends(get_current_user),
) -> schemas.User.DB:
    if not crud.user.is_admin(current_user):
        raise ValueError('PermissionDenied')
    return current_user


def get_current_root(
        current_user: schemas.User.DB = Depends(get_current_user),
) -> schemas.User.DB:
    if not crud.user.is_root(current_user):
        raise ValueError('PermissionDenied')
    return current_user
