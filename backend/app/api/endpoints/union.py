from typing import Any, List
from fastapi import APIRouter, Depends
from app import crud, schemas
from app.api import deps
from pymongo import MongoClient
from app.helpers import enum

router = APIRouter()


@router.post('/user/create', response_model=schemas.Union.Res, summary="[User] Create Union")
def create(
        *,
        m: MongoClient = Depends(deps.get_mongo),
        union_in: schemas.Union.Create,
        current_user: schemas.User.DB = Depends(deps.get_current_user)
) -> Any:
    insert_result = crud.union.create(m, obj_in=schemas.Union.Base(
        **union_in.model_dump(),
        admins=[current_user.id]
    ))
    # update user after union is created
    crud.user.update(m, id=current_user.id, obj_in={
        "unions": current_user.unions + [insert_result.inserted_id]
    })
    return crud.union.first_by_id(m, id=insert_result.inserted_id)

@router.put('/user/update/{id}', response_model=schemas.Union.Res, summary="[User] Update Union")
def update(
        *,
        m: MongoClient = Depends(deps.get_mongo),
        id: str,
        union_in: schemas.Union.Update,
        current_user: schemas.User.DB = Depends(deps.get_current_user)
) -> Any:
    union = crud.union.first(m, query=schemas.QueryBase(
        filters={
            "_id": crud.build_object_id(id),
            "admins": current_user.id
        }
    ))
    assert union is not None, "Union not found or user has no permission"
    print("union: ", union.id)
    crud.union.update(m, id=union.id, obj_in=union_in.model_dump())
    # update user after union is created
    return crud.union.first_by_id(m, id=union.id)

@router.post('/user/apply', response_model=schemas.Apply.Res, summary="[User] Apply to join Union")
def apply(
        *,
        m: MongoClient = Depends(deps.get_mongo),
        apply_in: schemas.Apply.Apply,
        current_user: schemas.User.DB = Depends(deps.get_current_user)
) -> Any:
    insert_result = crud.apply.create(m, obj_in=schemas.Apply.Base(
        **apply_in.model_dump(),
        applicant=current_user.id,
        status=enum.ReviewStatus.PENDING
    ))
    return crud.apply.first_by_id(m, id=insert_result.inserted_id)


@router.post('/user/review', response_model=schemas.Apply.Res, summary="[User] Review a join application")
def review(
        *,
        m: MongoClient = Depends(deps.get_mongo),
        review: schemas.Apply.Review,
        current_user: schemas.User.DB = Depends(deps.get_current_user)
) -> Any:
    a = crud.apply.first_by_id(m, id=review.apply_id)
    assert crud.union.is_admin(m, user_id=current_user.id, union_id=a.union), 'PermissionDenied'

    crud.apply.update(m, id=a.id, obj_in={
        "status": review.status,
        "rejected_reason": review.rejected_reason
    })

    # if approve, update user
    if a.status == enum.ReviewStatus.APPROVED:
        applicant = crud.user.first_by_id(m, id=a.applicant)
        if a.union not in applicant.unions:
            crud.user.update(m, id=a.applicant, obj_in={
                "unions": applicant.unions + [a.union]
            })

    return crud.apply.first_by_id(m, id=a.id)


@router.get('/user/list', response_model=List[schemas.Union.Res], summary="[User] List Unions")
def list(
        *,
        m: MongoClient = Depends(deps.get_mongo),
        skip: int,
        limit: int,
        current_user: schemas.User.DB = Depends(deps.get_current_user)
) -> Any:
    res = crud.union.get_multi(m, query=schemas.QueryBase(
        skip=skip,
        limit=limit,
        filters={
        "_id": {
            '$in': current_user.unions
        },
    }
    ))
    return res


@router.get('/user/list/apply', response_model=List[schemas.Apply.Res], summary="[User] List Review Unions")
def list_applies(
        *,
        m: MongoClient = Depends(deps.get_mongo),
        skip: int,
        limit: int,
        current_user: schemas.User.DB = Depends(deps.get_current_user)
) -> Any:
    unions = schemas.QueryBase.loop(crud.union.get_multi, m, query=schemas.QueryBase(
        filters={
        "_id": {
            '$in': current_user.unions
        },
        "admins": current_user.id
    }))
    applies = crud.apply.get_multi(m, query=schemas.QueryBase(
        filters={
            "union": {
                "$in": [u.id for u in unions]
            }
        },
        limit=limit,
        skip=skip
    ))
    dicts_ = [a.model_dump() for a in applies]
    for dict_ in dicts_:
        dict_["union_name"] = [u for u in unions if u.id == dict_["union"]][0].name
        user = crud.user.first(m, query=schemas.QueryBase(filters={
            "_id": dict_["applicant"]
        }))
        dict_["applicant_name"] = user.full_name
        dict_["applicant_phone"] = user.phone
    return dicts_


@router.get('/public/obj', response_model=schemas.Union.Res, summary="[Public] Get Union")
def get(
        *,
        m: MongoClient = Depends(deps.get_mongo),
        id: str,
) -> Any:
    res = crud.union.first(m, query=schemas.QueryBase(
        id=id
    ))
    return res