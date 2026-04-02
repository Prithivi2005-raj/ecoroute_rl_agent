import requests

BASE_URL = "http://127.0.0.1:8000"

# Reset environment
reset_response = requests.post(f"{BASE_URL}/reset")
print("RESET RESPONSE:")
print(reset_response.json())
print()

# IMPORTANT: action must be wrapped inside "action"
payload = {
    "action": {
        "transport_mode": "cycle",
        "traffic_level": 4,
        "distance_km": 6.0
    }
}

step_response = requests.post(f"{BASE_URL}/step", json=payload)
print("STEP RESPONSE:")
print(step_response.json())
print()

# Check state
state_response = requests.get(f"{BASE_URL}/state")
print("STATE RESPONSE:")
print(state_response.json())