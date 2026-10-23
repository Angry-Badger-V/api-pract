from datetime import datetime
from pydantic import BaseModel

class EventSummary(BaseModel):
    id: int
    title: str
    starts_at: datetime
    ends_at: datetime
    location: str | None

class EventDetail(BaseModel):
    id: int
    title: str
    description: str | None
    starts_at: datetime
    ends_at: datetime
    organiser_id: int | None
    venue_id: int | None
    created_at: datetime | None

class RsvpDetail(BaseModel):
    id: int
    attendee_id: int
    event_id: int
    created_at: datetime

class EventsResponse(BaseModel):
    events: list[EventSummary]

class EventResponse(BaseModel):
    event: EventDetail

class EventRsvpResponse(BaseModel):
    rsvp: RsvpDetail
