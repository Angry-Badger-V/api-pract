from datetime import datetime
from pydantic import BaseModel, EmailStr

class EventCreate(BaseModel):
    title: str
    description: str | None
    starts_at: datetime
    ends_at: datetime
    venue_id: int

class EventUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    starts_at: datetime | None = None
    ends_at: datetime | None = None
    venue_id: int | None = None

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

class EventAttendee(BaseModel):
    id: int
    name: str
    email: EmailStr

class RsvpDetail(BaseModel):
    id: int
    attendee_id: int
    event_id: int
    created_at: datetime

class EventCreateResponse(BaseModel):
    event: EventDetail

class EventsResponse(BaseModel):
    events: list[EventSummary]

class EventResponse(BaseModel):
    event: EventDetail

class EventRsvpResponse(BaseModel):
    rsvp: RsvpDetail

class EventUpdateResponse(BaseModel):
    event: EventDetail

class EventAttendeeResponse(BaseModel):
    attendees: list[EventAttendee]
