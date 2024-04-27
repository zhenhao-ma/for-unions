from enum import Enum


class Role(str, Enum):
    ROOT = 'ROOT'
    ADMIN = 'ADMIN'
    USER = 'USER'


class Country(str, Enum):
    CN = 'CN'
    US = 'US'
    UK = 'UK'


class ReviewStatus(str, Enum):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'

class ConnectType(str, Enum):
    CLOSED = 'CLOSED'
    REQUIRE_APPROVE = 'REQUIRE_APPROVE'
    OPEN = 'OPEN'
