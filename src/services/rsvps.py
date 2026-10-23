import src.repositories.rsvps as rsvp_repo

def rsvp_to_event(event_id: int, attendee_id: int):
    event_rsvps = rsvp_repo.select_rsvps(event_id)
    
    seen_ids = set()
    for event_rsvp in event_rsvps:
        seen_ids.add(event_rsvp["attendee_id"])
        if attendee_id in seen_ids:
            return None
    
    return rsvp_repo.insert_rsvp(event_id, attendee_id) 
