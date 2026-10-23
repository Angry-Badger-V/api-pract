import src.repositories.rsvps as rsvp_repo

def rsvp_exists(event_id: int, attendee_id: int) -> bool:
    event_rsvps = rsvp_repo.select_rsvps(event_id)

    return any(
        rsvp["attendee_id"] == attendee_id
        for rsvp in event_rsvps
    )

def rsvp_to_event(event_id: int, attendee_id: int):
    if rsvp_exists(event_id, attendee_id):
        return None

    return rsvp_repo.insert_rsvp(event_id, attendee_id)

def unrsvp_to_event(event_id: int, attendee_id: int):
    if not rsvp_exists(event_id, attendee_id):
        return None

    return rsvp_repo.delete_rsvp(event_id, attendee_id)
