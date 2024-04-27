from typing import Any
from fastapi import APIRouter, Depends
from app import crud, schemas, db
from app.api import deps
from pymongo import MongoClient
from typing import Optional, List
from app.helpers import wemini
from app.core.config import settings, Environment
from app.helpers import generate_random_string
from datetime import timedelta
from app.core import security

router = APIRouter()

access_token_key = f'wechat_app_access_token'


def _get_phone_login_cache_key(phone: str):
    return 'LOGIN_WITH_PHONE__{}'.format(phone)


@router.get('/public/wemini/get_phone', summary='[Public] Wechat App Get Phone Number',
            response_model=schemas.Wechat.PhoneInfoPublic)
def wechat_app_get_phone(*, wx_code: str):
    # get access token
    redis = db.get_redis()
    # get phone
    phone_res = wemini.get_phone_number(redis, secret=settings.WECHAT_APP_SECRET, appid=settings.WECHAT_APP_ID,
                                        code=wx_code)

    if phone_res.phone_info is None:
        raise ValueError(str(phone_res.model_dump()))

    # save cache to allow phone not verified to login
    phone = phone_res.phone_info.purePhoneNumber

    secret = generate_random_string(50)
    redis.set(_get_phone_login_cache_key(phone), secret, 5 * 60)

    return {
        'phone': phone,
        'secret': secret
    }


@router.get('/public/wemini/login', summary='[Public] Login, only for wechat user', response_model=schemas.Token)
def wechat_login(*,
                 m: MongoClient = Depends(deps.get_mongo),
                 js_code: str,
                 phone: str,
                 secret: str
                 ):

    # get session key
    session_response = wemini.js_code_to_session(js_code)
    if session_response.session_key is None:
        raise ValueError('Failed to retrieve session_key')
    if session_response.openid is None:
        raise ValueError('Failed to retrieve openid')

    # update or create user
    current_user = crud.user.first_by_phone(m, phone=phone)

    redis_client = db.get_redis()
    key = _get_phone_login_cache_key(phone)
    h = redis_client.get(key)

    if secret != h and settings.ENV == Environment.production:
        raise ValueError('Invalid code')
    else:
        redis_client.delete(key)

    # code matched

    if current_user is None:
        obj_in = schemas.User.Base(phone=phone, openid=session_response.openid,
                                   wechat_session_key=session_response.session_key)
        insert_result = crud.user.create(m, obj_in=obj_in)
        current_user = crud.user.first_by_id(m, id=insert_result.inserted_id)
    else:
        # update user
        upsert_res = crud.user.update(m, id=current_user.id, obj_in={
            "openid": session_response.openid,
            "wechat_session_key": session_response.session_key
        })
        current_user = crud.user.first_by_id(m, id=current_user.id)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return {
        "access_token": security.create_access_token(current_user.id, expires_delta=access_token_expires),
        "token_type": "bearer",
        'user': current_user
    }


@router.get('/user', summary='[User] Get Self',
            response_model=schemas.User.ResDetailed)
def get_self_by_access_token(*,
                             current_user: schemas.User.DB = Depends(deps.get_current_user)
                             ):
    return current_user


@router.put('/user', summary='[User] Update Self',
            response_model=schemas.User.ResDetailed)
def update_self(*,
                m: MongoClient = Depends(deps.get_mongo),
                user_in: schemas.User.Update,
                current_user: schemas.User.DB = Depends(deps.get_current_user)
                ):
    crud.user.update(m, id=current_user.id, obj_in=user_in.model_dump(exclude_unset=True))
    return crud.user.first_by_id(m, id=current_user.id)


@router.get('/public/list', summary='[Public] List Users',
            response_model=List[schemas.User.ResPreview])
def get_multi(*,
              m: MongoClient = Depends(deps.get_mongo),
              union_id: Optional[str],
              skip: int,
              limit: int
              ):
    users = crud.user.get_multi(m, query=schemas.QueryBase(skip=skip, limit=limit,
                                                           filters={
                                                               "unions": schemas.ObjectId(union_id)
                                                           } if union_id is not None else {}
                                                           ))

    return users
