from fastapi import APIRouter, HTTPException, Depends

from src.services import events as event_service
from src.services import rsvps as rsvp_service
from src.schemas.events import (
    EventsResponse,
    EventResponse,
    EventRsvpResponse
)

from src.dependencies.auth import get_current_user

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

@router.post("/{event_id}/rsvp", response_model=EventRsvpResponse)
def post_user_rsvp_to_event(event_id: int,
                            attendee_id: int = Depends(get_current_user)):
    event = event_service.get_event_by_id(event_id)
    
    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    rsvp = rsvp_service.rsvp_to_event(event_id, attendee_id)

    if rsvp is None:
        raise HTTPException(
            status_code=409,
            detail="Attendee has already RSVPed"
        )

    return {"rsvp": rsvp} 
