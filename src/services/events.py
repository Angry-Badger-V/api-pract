from datetime import datetime
from src.repositories import events as event_repo

def get_all_events() -> list[dict]:
    return event_repo.select_all_events()

def get_event_by_id(event_id: int) -> dict | None:
    return event_repo.select_event(event_id)

def make_new_event(title: str, description: str|None,
                starts_at: datetime, ends_at: datetime,
                organiser_id: int, venue_id: int):
    return event_repo.insert_event(title, description,
            starts_at, ends_at, organiser_id, venue_id)
