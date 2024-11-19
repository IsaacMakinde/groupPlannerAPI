import requests
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

ENDPOINT = os.getenv("API_TEST_ENDPOINT")

print(f"ENDPOINT: {ENDPOINT}/images")
print("Loaded API_TEST_ENDPOINT:", os.getenv("API_TEST_ENDPOINT"))
print("System-level API_TEST_ENDPOINT:", os.environ.get("API_TEST_ENDPOINT"))

def test_can_call_endpoint():
    response = requests.get(f"{ENDPOINT}/images")
    assert response.status_code == 200