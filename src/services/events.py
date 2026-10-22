from src.repositories import events as event_repo

def get_all_events() -> list[dict]:
    return event_repo.select_all_events()

def get_event_by_id(event_id: int) -> dict | None:
    return event_repo.select_event(event_id)
