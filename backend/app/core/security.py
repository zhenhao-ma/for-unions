from datetime import datetime, timedelta
import json
from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_access_token(
    user_id: str, expires_delta: timedelta = None
) -> str:
    """
    Create Access Token from subject
    :param user_id:
    :param expires_delta: How long will the password expired
    :return:
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": json.dumps({
        'user_id': user_id if isinstance(user_id, str) else str(user_id),
    })}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt