from psycopg2.extras import RealDictCursor
from db.connection import get_connection

def select_user_by_email(email: str) -> dict | None:
    conn = get_connection()

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT *
                FROM users
                WHERE email = %s;
            """, (email,))

            user = cursor.fetchone()
            return dict(user) if user else None

    finally:
        conn.close()

def insert_user(name: str, email: str, password_hash: str) -> dict:
    conn = get_connection()

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                INSERT INTO users (name, email, password)
                VALUES (%s, %s, %s)
                RETURNING id, name, email, created_at;
            """, (name, email, password_hash))

            user = dict(cursor.fetchone())

        conn.commit()
        return user

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()
