from fastapi import HTTPException

from src.services import events as event_service

def get_valid_event(event_id: int):
    event = event_service.get_event_by_id(event_id)

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    return event
