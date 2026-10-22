import os
from fastapi import Query
import jwt
import datetime
from argon2 import PasswordHasher
from argon2.exceptions import (
    VerifyMismatchError,
    VerificationError,
    InvalidHashError,
)
from psycopg2.extras import RealDictCursor

from db.connection import get_connection

ph = PasswordHasher()

SECRET_KEY = os.environ["JWT_SECRET_KEY"]
ALGORITHM = os.environ["JWT_ALGO"]

def user_insert(user: dict) -> None:
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                INSERT INTO users (name, email, password)
                VALUES (%s, %s, %s);
            """, (user["name"], user["email"], user["password"],))
        conn.commit()
    except Exception:
        conn.rollback()
    finally:
        conn.close()

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

def normalise_user(user: dict) -> None:
    name_normalisation(user)
    email_normalisation(user)
    password_hashing(user)
    
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
