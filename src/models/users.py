from psycopg2.extras import RealDictCursor

from db.connection import get_connection
from pydantic import BaseModel

import src.seed.users as user_util

class User(BaseModel):
    name: str#,

class UserAuth(BaseModel):
    email: str
    password: str

def select_user_by_email(user_auth: UserAuth) -> dict:
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT * FROM users
                WHERE email = %s;
            """, (user_auth.email,))
            user = cursor.fetchone()
            return user

    finally:
        conn.close()   

def authorise_user(user_auth: UserAuth) -> str|None:
    user = select_user_by_email(user_auth)
    if user is None:
        return None
    return user_util.password_authorise(user["email"], user_auth.password, user["password"])
