import uuid
import string
import random
from pydantic import BaseModel

def id_generator() -> str:
    return str(uuid.uuid4())


def generate_random_string(length: int = 32, *, lower: bool = True, upper: bool = True, digit: bool = True) -> str:
    candidates = []
    if lower: candidates += string.ascii_lowercase
    if upper: candidates += string.ascii_uppercase
    if digit: candidates += string.digits
    assert len(candidates) > 0, 'Invalid random string generator, missing candidates.'
    return ''.join(random.choice(candidates) for i in range(length))

def is_pydantic_field_empty(obj: BaseModel, field: str) -> bool:
    return not hasattr(obj, field) or getattr(obj, field) is None

