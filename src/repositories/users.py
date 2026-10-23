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

def select_user_events(user_id: int) -> list[dict]:
    conn = get_connection()

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT
                    e.id,
                    e.title,
                    e.starts_at,
                    r.created_at AS rsvp_date,
                    ROW_NUMBER() OVER (
                        ORDER BY e.starts_at ASC, e.id ASC
                    ) AS event_rank,
                    (
                        SELECT COUNT(*)
                        FROM rsvps
                        WHERE event_id = e.id
                    ) AS total_rsvps
                FROM events AS e
                JOIN rsvps AS r
                    ON r.event_id = e.id
                WHERE r.attendee_id = %s
                ORDER BY e.starts_at ASC, e.id ASC;
            """, (user_id,))

            events = [
                dict(event) for event in cursor.fetchall()
            ]

        return events

    finally:
        conn.close()
