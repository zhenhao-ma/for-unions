from enum import Enum
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from typing import List

class Environment(str, Enum):
    development = 'development'
    test = 'test'
    production = 'production'


class Settings(BaseSettings):
    VERSION: str = '1.0.0'
    API_V1_STR: str = "/api/v1"

    ENV: Environment = Environment.development

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ['http://127.0.0.1:3000', 'http://127.0.0.1:4000', 'http://localhost:4000',
                                              'http://127.0.0.1:8080', 'http://0.0.0.0:8000']

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 525600
    SECRET_KEY: str = 'SECRET_KEY'

    # Redis
    REDIS_URI: str

    # Mongo DB
    MONGO_DB_URI: str
    MONGO_DB_DATABASE: str

    # WECHAT
    WECHAT_APP_ID: str
    WECHAT_APP_SECRET: str


    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()