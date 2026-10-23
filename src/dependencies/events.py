from fastapi import Depends, HTTPException

from src.dependencies.auth import get_current_user
from src.services import events as event_service

def get_valid_event(event_id: int):
    event = event_service.get_event_by_id(event_id)

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    return event

def get_organiser_event(event=Depends(get_valid_event), organiser_id=Depends(get_current_user)):
    if event["organiser_id"] != organiser_id:
        raise HTTPException(
            status_code=403,
            detail="You are not the organiser of this event"
        )
    return event
