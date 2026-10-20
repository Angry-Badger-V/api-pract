
import json
from pathlib import Path

from fastapi.testclient import TestClient
from main import app


client = TestClient(app, follow_redirects=False)

DATA_PATH = "db/data/events.json"


def get_seed_events():
    with open(DATA_PATH, "r") as file:
        return json.load(file)


def test_get_events_returns_200():
    response = client.get("/api/events")

    assert response.status_code == 200


def test_get_events_returns_events_key():
    response = client.get("/api/events")

    body = response.json()

    assert isinstance(body, dict)
    assert "events" in body
    assert isinstance(body["events"], list)


def test_get_events_returns_all_seeded_events():
    response = client.get("/api/events")

    events = response.json()["events"]
    seeded_events = get_seed_events()

    assert len(events) == len(seeded_events)

    returned_titles = sorted(
        event["title"] for event in events
    )

    expected_titles = sorted(
        event["title"] for event in seeded_events
    )

    assert returned_titles == expected_titles


def test_get_events_have_required_fields():
    response = client.get("/api/events")

    events = response.json()["events"]

    assert len(events) > 0

    for event in events:
        assert "id" in event
        assert "title" in event
        assert "starts_at" in event
        assert "ends_at" in event
        assert "location" in event


def test_events_are_ordered_by_start_date():
    response = client.get("/api/events")

    events = response.json()["events"]

    expected_order = sorted(
        events,
        key=lambda event: (
            event["starts_at"],
            event["id"]
        )
    )

    assert events == expected_order


def test_get_events_returns_correct_data_types():
    response = client.get("/api/events")

    events = response.json()["events"]

    for event in events:
        assert isinstance(event["id"], int)
        assert isinstance(event["title"], str)
        assert isinstance(event["starts_at"], str)
        assert isinstance(event["ends_at"], str)

        assert (
            event["location"] is None
            or isinstance(event["location"], str)
        )
