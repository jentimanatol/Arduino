import requests
import json
from datetime import datetime
import os

# ----------------------- Configuration -----------------------

API_CREDENTIALS = {
    "client_id": "Jr3t1Lgx5LIjDzPKCQ9Y8AUkI27RBjzv",
    "client_secret": "1OgQhAVeFXgwwvPRzJDyY1wE9p6kq3ssnmnXiPRZnd1S1JBnjFloWhqDbQkGkxZd",
    "audience": "https://api2.arduino.cc/iot"
}

JSON_FILE = "arduino_garden_log.json"

# Arduino Cloud API endpoints
BASE_URL = "https://api2.arduino.cc/iot/v2"
AUTH_URL = f"{BASE_URL}/oauth/token"
THINGS_URL = f"{BASE_URL}/things"

# Property ID map (UUIDs)
PROPERTY_MAP = {
    "7d2008e2-25d9-4a4b-9038-cbeb93b5672f": "Water Switch",
    "9ee5a505-d461-480c-983b-a02449fe6ea8": "Temperature Sensor (°C)",
    "a800f920-4961-4853-85fb-43abbbaf303a": "Water Status",
    "c54f0268-39b2-4334-a8aa-11f620107580": "Soil Moisture (%)",
    "d426bf72-0a03-426b-8c43-7b32b99dc530": "Air Humidity (%)",
    "8da7aae6-7f40-435c-ba7e-9c8a39d835bd": "Water Valve"
}

# ----------------------- Auth Function -----------------------

def get_auth_token():
    print("🔑 Requesting access token...")
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": API_CREDENTIALS["client_id"],
        "client_secret": API_CREDENTIALS["client_secret"],
        "audience": API_CREDENTIALS["audience"]
    }
    response = requests.post(AUTH_URL, headers=headers, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

# ----------------------- Data Fetching -----------------------

def get_things(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(THINGS_URL, headers=headers)
    response.raise_for_status()
    return response.json()

def get_property_value(token, thing_id, property_id):
    url = f"{THINGS_URL}/{thing_id}/properties/{property_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get("last_value")

# ----------------------- JSON Handling -----------------------

def load_existing_data():
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Corrupted JSON file, starting fresh.")
    return {"garden_log": []}

def save_data(data):
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Data logged to {JSON_FILE}")

# ----------------------- Main Collector -----------------------

def collect_sensor_data():
    print("\nStarting garden data collection...")
    token = get_auth_token()
    things = get_things(token)

    if not things:
        print("🚫 No things found in your Arduino IoT Cloud account.")
        return

    thing = things[0]  # Grab the first thing (your device)
    thing_id = thing["id"]

    # Fetch values for each property
    reading = {
        "timestamp": datetime.now().isoformat(),
        "data": {}
    }

    for property_id, label in PROPERTY_MAP.items():
        try:
            value = get_property_value(token, thing_id, property_id)
            reading["data"][label] = value
            print(f"📥 {label}: {value}")
        except requests.exceptions.RequestException as e:
            reading["data"][label] = None
            print(f" Error reading {label}: {e}")

    # Append and save
    all_data = load_existing_data()
    all_data["garden_log"].append(reading)
    save_data(all_data)

# ----------------------- Run Once -----------------------

if __name__ == "__main__":
    collect_sensor_data()
