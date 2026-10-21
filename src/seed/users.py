import os
import jwt
import datetime
from argon2 import PasswordHasher
from argon2.exceptions import (
    VerifyMismatchError,
    VerificationError,
    InvalidHashError,
)

ph = PasswordHasher()

SECRET_KEY = os.environ["JWT_SECRET_KEY"]
ALGORITHM = os.environ["JWT_ALGO"]

def name_normalisation(user: dict) -> None:
    user["name"] = " ".join(
            user["name"].split())

def email_normalisation(user: dict) -> None:
    user["email"] = "".join(
            user["email"].split()
            ).lower()
    
def password_hashing(user: dict) -> None:
    user["password"] = ph.hash(
            user["password"])
    
def password_authorise(email: str, password: str, hashed_password: str) -> str|None:
    print(f"email: {email}\nhased: {hashed_password}\npass: {password}")
    try:
        ph.verify(hashed_password, password)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return None
    token = jwt.encode(
        {
            "sub": email,
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=20)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return token
