from warnings import resetwarnings

from psycopg2.extras import RealDictCursor
from db.connection import get_connection

def select_rsvps(event_id: int) -> list[dict]:
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT 
                    id,
                    attendee_id,
                    event_id,
                    created_at
                FROM rsvps
                WHERE event_id = %s;
            """, (event_id,))

            event_rsvps = cursor.fetchall()

            return [dict(rsvp) for rsvp in event_rsvps]

    finally:
        conn.close()

def insert_rsvp(event_id: int, attendee_id: int) -> dict:
    conn = get_connection()

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                INSERT INTO rsvps (attendee_id, event_id)
                VALUES (%s, %s)
                RETURNING id, attendee_id, event_id, created_at;
            """, (attendee_id, event_id))

            rsvp = dict(cursor.fetchone())

        conn.commit()
        return rsvp
    
    except Exception:
        conn.rollback()
        raise
    
    finally:
        conn.close()

def delete_rsvp(event_id: int, attendee_id: int) -> dict:
    conn = get_connection()

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                DELETE FROM rsvps 
                WHERE event_id = %s
                AND attendee_id = %s
                RETURNING id, attendee_id, event_id, created_at;
            """, (event_id, attendee_id))
            
            result = cursor.fetchone()
            rsvp = dict(result) if result else None

        conn.commit()
        return rsvp
    
    except Exception:
        conn.rollback()
        raise
    
    finally:
        conn.close()
