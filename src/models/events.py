from db.connection import get_connection
from psycopg2.extras import RealDictCursor

def select_all_events():
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

def select_event(id):
    conn = get_connection()

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT
                    e.*
                FROM
                    events e
                WHERE
                    e.id = %s
            """, (id,))

            event = cursor.fetchone()

            return event
    
    finally:
        conn.close()
