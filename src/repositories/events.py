from datetime import datetime
from db.connection import get_connection
from psycopg2.extras import RealDictCursor

def select_all_events() -> list[dict]:
    conn = get_connection()

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT
                    e.id,
                    e.title,
                    e.starts_at,
                    e.ends_at,
                    v.address AS location
                FROM events AS e
                LEFT JOIN venues AS v
                    ON e.venue_id = v.id
                ORDER BY e.starts_at ASC, e.id ASC;
            """)

            events = cursor.fetchall()

            return [dict(event) for event in events]

    finally:
        conn.close()

def select_event(event_id: int) -> dict | None:
    conn = get_connection()

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT *
                FROM events
                WHERE id = %s;
            """, (event_id,))

            event = cursor.fetchone()

            return dict(event) if event else None

    finally:
        conn.close()

def insert_event(title: str, description: str|None,
                 starts_at: datetime, ends_at: datetime,
                 organiser_id: int, venue_id: int) -> dict:
    conn = get_connection()

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                INSERT INTO events (title, description,
                    starts_at, ends_at, organiser_id, venue_id) 
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id, title, description,
                starts_at, ends_at, organiser_id, venue_id, created_at;
            """, (title, description, starts_at, ends_at,
                  organiser_id, venue_id))

            event = dict(cursor.fetchone())

        conn.commit()
        return event
    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()
