from db.connection import get_connection
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, HTTPException
from src.models.events import select_all_events, select_event
from src.models.users import UserAuth, authorise_user

app = FastAPI()

@app.get("/api/events")
def get_events():
    events = select_all_events()
    return {"events": events}

@app.get("/api/events/{id}")
def get_events(id: int):
    event = select_event(id)
    return {"event": event}

@app.post("/api/auth/login")
def get_hash(user_auth: UserAuth):
    token = authorise_user(user_auth)
    if token is None:
        raise HTTPException(
                status_code=401,
                detail="Invalid email or password")
    return {"token": token}
