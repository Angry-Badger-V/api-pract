import os
import jwt
import datetime

from argon2 import PasswordHasher
from argon2.exceptions import (
    VerifyMismatchError,
    VerificationError,
    InvalidHashError
)

ph = PasswordHasher()

SECRET_KEY = os.environ["JWT_SECRET_KEY"]
ALGORITHM = os.environ["JWT_ALGO"]

def hash_password(password: str) -> str:
    return ph.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    try:
        return ph.verify(hashed_password, password)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False

def create_access_token(email: str) -> str:
    return jwt.encode(
        {
            "sub": email,
            "exp": datetime.datetime.now(
                datetime.timezone.utc
            ) + datetime.timedelta(minutes=20)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )
