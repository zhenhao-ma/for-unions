from typing import Any
from fastapi import APIRouter, Depends
from app import crud, schemas, db
from app.api import deps
from pymongo import MongoClient
from app.core.config import settings
from datetime import timedelta
from app.core import security
import random
from app.helpers import enum
from app.helpers import generate_random_string

router = APIRouter()


@router.get('/get_token', response_model=schemas.Token)
def register_in_public_scope(
        *,
        m: MongoClient = Depends(deps.get_mongo),
        phone: str = None
) -> Any:
    if phone is not None:
        current_user = crud.user.first_by_phone(m, phone=phone)
        if current_user is None:
            # create user
            obj_in = schemas.User.Base(phone=phone, openid=None,
                                       wechat_session_key=None)
            insert_result = crud.user.create(m, obj_in=obj_in)
            current_user = crud.user.first_by_id(m, id=insert_result.inserted_id)
    else:
        # default first user
        current_user = crud.user.first(m, query=schemas.QueryBase())

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return {
        "access_token": security.create_access_token(current_user.id, expires_delta=access_token_expires),
        "token_type": "bearer",
        'user': current_user
    }


@router.get('/random_applies', response_model=schemas.Status)
def create_random_applicants(
        *,
        m: MongoClient = Depends(deps.get_mongo),
        current_user: schemas.User.DB = Depends(deps.get_current_user)
) -> Any:
    all_unions = schemas.QueryBase.loop(crud.union.get_multi, m, query=schemas.QueryBase(filters={
        "_id": {
            '$in': current_user.unions
        },
        "admins": current_user.id
    }))
    # create random application
    for i in range(100):
        union = random.choice(all_unions)
        new_user = schemas.User.Base(
            phone=generate_random_string(length=13, digit=True, upper=False, lower=False),
        )
        insert_result = crud.user.create(m, obj_in=new_user)
        db_user = crud.user.first_by_id(m, id=insert_result.inserted_id)
        apply = schemas.Apply.Base(
            union=union.id,
            desciption=generate_random_string(length=32),
            applicant=db_user.id,
            status=enum.ReviewStatus.PENDING
        )
        crud.apply.create(m, obj_in=apply)

    return {
        "status": True
    }
