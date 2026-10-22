from fastapi import APIRouter, HTTPException

from src.services import events as event_service
from src.schemas.events import EventsResponse, EventResponse


router = APIRouter(
    prefix="/api/events",
    tags=["Events"]
)

@router.get("", response_model=EventsResponse)
def get_events():
    events = event_service.get_all_events()

    return {"events": events}

@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: int):
    event = event_service.get_event_by_id(event_id)

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    return {"event": event}
