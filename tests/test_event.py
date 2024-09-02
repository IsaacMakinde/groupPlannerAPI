import requests
from dotenv import load_dotenv
import os
import uuid


load_dotenv()

ENDPOINT = os.getenv("API_TEST_ENDPOINT")
## delete all events
print(f"ENDPOINT: {ENDPOINT}")
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
  "category": "Celebration",
  "date": "2024-12-12",
  "description": "Test",
  "guests":"Test guest",
  "host": "Test host ",
  "pricing": 10.0,
  "title": unique_title, ##  have to constantly change this
  "venue": "Test Venue"
}
    create_event_response = create_event(payload)
    assert create_event_response.status_code == 201
    data = create_event_response.json()
    print(data)

    event_id = data['id']
    get_event_response = get_event(event_id)


    assert get_event_response.status_code == 200
    get_event_data = get_event_response.json()
    assert get_event_data['title'] == payload['title']
    assert get_event_data['date'] == payload['date']

def test_given_valid_data_can_update_event():
    # create a new event
    event_id, original_payload = create_update_test_event_valid()

    # update the event with new data
    update_payload ={
        "date": "2024-10-12",
        "description": "Test for updating new events",
        "pricing": 40.0,
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


    # check the original data
    assert updated_data['title'] == original_payload['title']
    assert updated_data['host'] == original_payload['host']
    assert updated_data['venue'] == original_payload['venue']
    assert updated_data['category'] == original_payload['category']
    assert updated_data['guests'] == original_payload['guests']
    assert updated_data['id'] == event_id

def test_update_with_invalid_data():
    """Test updating an event with invalid data should fail."""
    event_id, _  = create_update_test_event_invalid()
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
  "date": "2024-12-12",
  "description": "Test for creating new events",
  "guests":"Test guest",
  "host": "Test host ",
  "pricing": 10.0,
  "title": unique_title,
  "venue": "Test Venue"
}


def create_update_test_event_valid():
    """Helper function to create a test event"""
    unique_title = f"Test Title-{uuid.uuid4()}"
    payload = {
        "category": "Travel",
        "date": "2024-12-25",
        "description": "Test for updating events",
        "guests":"Test guest",
        "host": "Test host ",
        "pricing": 10.0,
        "title": unique_title,
        "venue": "Test Venue"
    }
    response = create_event(payload)
    assert response.status_code == 201
    return response.json()["id"], payload


def create_update_test_event_invalid():
    """Helper function to create a test event"""
    unique_title = f"Test Title-{uuid.uuid4()}"
    payload = {
        "category": "Travel",
        "date": "2024-12-25",
        "description": "Test for updating events given invalid data",
        "guests":"Test guest",
        "host": "Test host ",
        "pricing": 10.0,
        "title": unique_title,
        "venue": "Test Venue"
    }
    response = create_event(payload)
    assert response.status_code == 201
    return response.json()["id"], payload

def delete_events():
    return requests.delete(f"{ENDPOINT}/events")

