import requests
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

ENDPOINT = os.getenv("API_TEST_ENDPOINT")
## delete all events
print(f"ENDPOINT: {ENDPOINT}/events")
print("Loaded API_TEST_ENDPOINT:", os.getenv("API_TEST_ENDPOINT"))
print("System-level API_TEST_ENDPOINT:", os.environ.get("API_TEST_ENDPOINT"))


def test_can_call_endpoint():
    response = requests.get(f"{ENDPOINT}/events")
    assert response.status_code == 200

def test_clean_db():
    response = requests.delete(f"{ENDPOINT}/events")
    assert response.status_code == 200

def test_can_get_empty_list():
    response = requests.get(f"{ENDPOINT}/events")
    data = response.json()
    assert len(data) == 0 and response.status_code == 200

def test_can_create_event():
    unique_title = f"Test Title-{uuid.uuid4()}"
    
    payload = {
    "title": unique_title,
    "clerk_id": 1,
    "host": "Isaac Gbolahan Makinde",
    "date": "2024-12-12",
    "venue": "Pink, William Street South, Dublin 2, Ireland",
    "place_id": "ChIJo4D-SZwOZ0gRe0UTV3vFnxI",
    "description": "This is a test description",
    "category" : "Travel",
    "pricing" : 10.99,
    "guests" : "Isaac, David, Nico"
        }
    create_event_response = create_event(payload)
    assert create_event_response.status_code == 201
    data = create_event_response.json()
    print(data)

    event_id = data["id"]
    print(event_id)

    get_event_response = get_event(event_id)
    assert get_event_response.status_code == 200
    get_event_data = get_event_response.json()
    print(get_event_data)
    assert get_event_data['title'] == payload['title']
    assert get_event_data['date'] == payload['date']

def test_given_valid_data_can_update_event():
    # create a new event
    event_id, original_payload = create_update_test_event_valid()

    # update the event with new data
    unique_title = f"Updated Title-{uuid.uuid4()}"
    update_payload = {
        "title": unique_title,
        "host": "Isaac Gbolahan Makinde",
        "clerk_id": 1,
        "date" : "2024-12-25",
        "venue": "Pink, William Street South, Dublin 2, Ireland",
        "place_id": "ChIJo4D-SZwOZ0gRe0UTV3vFnxI",
        "description": "This is a test fpr updating events",
        "category": "Travel",
        "pricing": 40.0,
        "guests": "Isaac, David, Nico, Josh, Shubham"
    }
    update_event_response = update_event(update_payload, event_id)
    assert update_event_response.status_code == 200

    # check the updated data
    updated_data = update_event_response.json()
    updated_data["pricing"] = float(updated_data["pricing"])
    assert type(updated_data['pricing']) == type(update_payload['pricing'])
    assert updated_data['pricing'] == update_payload['pricing']
    assert updated_data['date'] == update_payload['date']
    assert updated_data['description'] == update_payload['description']

def test_update_with_invalid_data():
    """Test updating an event with invalid data should fail."""
    event_id, current_payload = create_update_test_event_invalid()
    invalid_payload = {
        "date": "invalid-date-format",
        "pricing": "not-a-number"
    }
    update_event_response = update_event(invalid_payload, event_id)
    assert update_event_response.status_code == 400
    print(update_event_response.json())

    # check the original data
    
## helper functions
def create_event(payload):
    return requests.post(f"{ENDPOINT}/events", json=payload)

def get_event(event_id):
    return requests.get(f"{ENDPOINT}/events/{event_id}")

def update_event(payload, event_id):
    return requests.put(f"{ENDPOINT}/events/{event_id}", json=payload)


def new_event_payload():
    unique_title = f"Test Title-{uuid.uuid4()}"
    return {
  "category": "Celebration",
  "clerk_id": 1,
  "date": "2024-12-12",
  "description": "Test for creating new events",
  "guests":"testGuest1, TestGuest2",
  "host": "Isaac Gbolahan Makinde",
  "place_id": "ChIJo4D-SZwOZ0gRe0UTV3vFnxI",
  "pricing": 10.0,
  "title": unique_title,
  "venue": "Pink, William Street South, Dublin 2, Ireland"
}

def create_update_test_event_valid():
    """Helper function to create a test event"""
    unique_title = f"Test Title-{uuid.uuid4()}"
    payload = {
        "category": "Travel",
        "clerk_id": 1,
        "date": "2024-12-25",
        "description": "Test for updating events",
        "guests":"Isaac, Nico, David",
        "host": "Isaac Gbolahan Makinde",
        "place_id": "ChIJo4D-SZwOZ0gRe0UTV3vFnxI",
        "pricing": 10.0,
        "title": unique_title,
        "venue": "Pink, William Street South, Dublin 2, Ireland"
    }
    response = create_event(payload)
    assert response.status_code == 201
    return response.json()["id"], payload

def create_update_test_event_invalid():
    """Helper function to create a test event"""
    unique_title = f"Test Title-{uuid.uuid4()}"
    payload = {
        "category": "Travel",
        "clerk_id": 1,
        "date": "2024-12-25",
        "description": "Test for updating events given invalid data",
        "guests":"testGuest1, Test_guest2",
        "host": "Isaac Gbolahan Makinde ",
        "place_id": "ChIJo4D-SZwOZ0gRe0UTV3vFnxI",
        "pricing": 10.0,
        "title": unique_title,
        "venue": "Pink, William Street South, Dublin 2, Ireland"
    }
    response = create_event(payload)
    assert response.status_code == 201
    return response.json()["id"], payload

def delete_events():
    return requests.delete(f"{ENDPOINT}/events")

