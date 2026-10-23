from fastapi import APIRouter, HTTPException, Depends, Response

from src.services import events as event_service
from src.services import rsvps as rsvp_service

from src.schemas.events import (
    EventCreate,
    EventCreateResponse,
    EventUpdate,
    EventAttendee,
    EventUpdateResponse,
    EventsResponse,
    EventResponse,
    EventRsvpResponse,
    EventAttendeeResponse
)

from src.dependencies.auth import get_current_user
from src.dependencies.events import get_valid_event, get_organiser_event

router = APIRouter(
    prefix="/api/events",
    tags=["Events"]
)

@router.get("", response_model=EventsResponse)
def get_events():
    events = event_service.get_all_events()

    return {"events": events}

@router.post("", status_code=201, response_model=EventCreateResponse)
def post_event(event_details: EventCreate,
               organiser_id: int = Depends(get_current_user)):
    event = event_service.make_new_event(
        event_details.title,
        event_details.description,
        event_details.starts_at,
        event_details.ends_at,
        organiser_id,
        event_details.venue_id
    )
    return {"event": event}

@router.get("/{event_id}", response_model=EventResponse)
def get_event(event=Depends(get_valid_event)):
    return {"event": event}

@router.patch("/{event_id}", status_code=200, response_model=EventUpdateResponse)
def patch_event(event_update: EventUpdate,
            event=Depends(get_organiser_event)):
    patched_event = event_service.patch_event(event_id=event["id"],
        updates=event_update.model_dump(exclude_unset=True))

    return {"event": patched_event}

@router.get("/{event_id}/attendees",
            response_model=EventAttendeeResponse)
def get_attendees(event=Depends(get_organiser_event)):
    attendees = event_service.get_event_attendees(event_id=event["id"])
    return {"attendees": attendees}

@router.post("/{event_id}/rsvp", status_code=201,
    response_model=EventRsvpResponse)
def post_user_rsvp_to_event(event=Depends(get_organiser_event),
    attendee_id: int = Depends(get_current_user)):
    rsvp = rsvp_service.rsvp_to_event(
        event["id"],
        attendee_id
    )

    if rsvp is None:
        raise HTTPException(
            status_code=409,
            detail="Attendee has already RSVPed"
        )

    return {"rsvp": rsvp}

@router.delete("/{event_id}/rsvp", status_code=204)
def delete_user_rsvp_to_event(event=Depends(get_valid_event),
    attendee_id: int = Depends(get_current_user)):
    rsvp = rsvp_service.unrsvp_to_event(
        event["id"],
        attendee_id
    )

    if rsvp is None:
        raise HTTPException(
            status_code=404,
            detail="No RSVP exists for this attendee on this event"
        )

    return Response(status_code=204)
