from psycopg2.extras import RealDictCursor
from db.connection import get_connection
from pydantic import BaseModel

import src.seed.users as user_util

class UserAuth(BaseModel):
    email: str
    password: str

class UserReg(BaseModel):
    name: str
    email: str
    password: str

def select_user_by_email(user: dict) -> dict|None:
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT * FROM users
                WHERE email = %s;
            """, (user["email"],))
            user = cursor.fetchone()
            return user
    finally:
        conn.close()

def authorise_user(user_auth: UserAuth) -> str|None:
    user_email = {"email": user_auth.email}
    user_util.email_normalisation(user_email)
    user = select_user_by_email(user_email)
    if user is None:
        return None
    return user_util.password_authorise(user["email"], user_auth.password, user["password"])

def register_user(user_reg: UserReg) -> dict|None:
    user = {"name": user_reg.name, "email": user_reg.email, "password": user_reg.password} 
    user_util.normalise_user(user) 
    if select_user_by_email(user) is not None: # user already exists 409 Conflict
        return None
    user_util.user_insert(user)
    return select_user_by_email(user) # will return None if failed to insert # TODO: make this raise error other than 409 
