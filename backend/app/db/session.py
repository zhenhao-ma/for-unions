from redis import Redis as R, ConnectionPool
from app.core.config import settings
from pymongo import MongoClient

redis_pool = ConnectionPool.from_url(settings.REDIS_URI)


def get_redis():
    """Return conn to redis
    You do not need to explicitly close the redis conn"""
    return R(connection_pool=redis_pool)


def get_mongo():
    """Return a mongo conn
    You do not need to close PyMongo connections. Leave them open so that PyMongo connection pooling gives you the most efficient performance"""
    return MongoClient(settings.MONGO_DB_URI)