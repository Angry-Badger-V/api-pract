from fastapi import APIRouter
import src.models.events as events

router = APIRouter(
    prefix="/api/events",
    tags=["Events"]
)

@router.get("")
def get_events():
    all_events = events.select_all_events()
    return {"events": all_events}

@router.get("/{id}")
def get_event(id: int):
    event = events.select_event(id)
    return {"event": event}
