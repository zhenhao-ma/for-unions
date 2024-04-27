import time

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from app.api import api_router
from app.core.config import settings, Environment
import uvicorn as uvicorn
from app.helpers.exceptions import initialize_exception_handler


app = FastAPI(
    title=f"Doc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json" if settings.ENV != Environment.production else None,
    redoc_url=f'{settings.API_V1_STR}/redoc' if settings.ENV != Environment.production else None,
    docs_url=f'{settings.API_V1_STR}/docs' if settings.ENV != Environment.production else None,
    version=settings.VERSION,
    middleware=[]
)
# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        # allow_origin_regex='http://localhost:4000',
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


initialize_exception_handler(app)


@app.middleware("http")
async def add_global_http_process(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='0.0.0.0')
