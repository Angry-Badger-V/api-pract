from db.connection import get_connection
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI
from src.models.events import select_all_events

app = FastAPI()

@app.get("/api/events")
def get_events():
    events = select_all_events()
    return {"events": events}
