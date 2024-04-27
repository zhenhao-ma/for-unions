from fastapi import APIRouter
from app.core.config import settings, Environment
from app.api.endpoints import user, dev_only, union

api_router = APIRouter()

api_router.include_router(user.router, prefix='/user', tags=['user'])
api_router.include_router(union.router, prefix='/union', tags=['union'])

if settings.ENV == Environment.development:
    api_router.include_router(dev_only.router, prefix='/dev_only', tags=['dev_only'])
