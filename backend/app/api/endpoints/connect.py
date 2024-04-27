from typing import Any
from fastapi import APIRouter, Depends
from app import crud, schemas, db
from app.api import deps
from pymongo import MongoClient
from app.helpers import enum

router = APIRouter()


@router.post('/user/create', response_model=schemas.Connect.Res, summary="[User] Connect to others")
def create(
        *,
        m: MongoClient = Depends(deps.get_mongo),
        conn_in: schemas.Connect.Create,
        current_user: schemas.User.DB = Depends(deps.get_current_user)
) -> Any:
    c = crud.connect.get_connect(m, from_user=current_user.id, to_user=conn_in.to_user)

    if c is not None:
        return c
    to_user = crud.user.first_by_id(m, id=conn_in.to_user)
    assert to_user.connect_type != enum.ConnectType.CLOSED, 'PermissionDenied'
    # create new connect
    insert_res = crud.connect.create(m, obj_in=schemas.Connect.Base(
        from_user=current_user.id,
        to_user=conn_in.to_user,
        description=conn_in.description,
        status=enum.ReviewStatus.PENDING if to_user.connect_type == enum.ConnectType.REQUIRE_APPROVE else enum.ReviewStatus.APPROVED
    ))
    return crud.connect.first(m, query=insert_res.inserted_id)


@router.post('/user/review', response_model=schemas.Connect.Res, summary="[User] Review connect")
def create(
        *,
        m: MongoClient = Depends(deps.get_mongo),
        conn_in: schemas.Connect.Review,
        current_user: schemas.User.DB = Depends(deps.get_current_user)
) -> Any:
    c = crud.connect.first_by_id(m, id=conn_in.id)
    assert c.to_user == current_user.id, 'PermissionDenied'
    crud.connect.update(m, id=c.id, obj_in={
        "status": conn_in.status
    })

    return crud.connect.first(m, query=c.id)
