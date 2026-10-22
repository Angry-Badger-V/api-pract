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
