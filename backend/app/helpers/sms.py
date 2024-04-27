from app.helpers import common
from redis import Redis


def send_to(redis: Redis, *, phone: str) -> None:
    """Send code to phone, expire in 5 minutes"""
    key = __get_phone_key(phone)
    code = __get_new_code(redis, phone=phone)
    redis.set(key, code, 30)
    print('Sent Sms Code: {} to {}'.format(code, phone))


def varify(redis: Redis, *, phone: str, code: str) -> bool:
    key = __get_phone_key(phone)
    h = redis.get(key)
    return h == code.lower().strip()


def __get_phone_key(phone: str):
    return f'phone_key_{phone}'


def __get_new_code(redis: Redis, *, phone: str) -> str:
    """Get a sms code
    from cache, or generate a new one"""
    key = __get_phone_key(phone)
    h = redis.get(key)
    return h if h is not None else common.generate_random_string(4, lower=False, upper=False, digit=True)
