import requests
import json
import time
from datetime import datetime
import os

# ---- Configuration ----

API_CREDENTIALS = {
    "name": "BhccGardenApiKeys",
    "created_date": "April 15, 2025",
    "client_id": "Jr3t1Lgx5LIjDzPKCQ9Y8AUkI27RBjzv",
    "client_secret": "1OgQhAVeFXgwwvPRzJDyY1wE9p6kq3ssnmnXiPRZnd1S1JBnjFloWhqDbQkGkxZd",
    "audience": "https://api2.arduino.cc/iot"
}

BASE_URL = "https://api2.arduino.cc/iot/v2"
AUTH_URL = f"{BASE_URL}/oauth/token"
THINGS_URL = f"{BASE_URL}/things"

JSON_FILE = "arduino_garden_data.json"

# Replace with your real Thing ID and Variable IDs
THING_ID = "your-thing-id-here"  # Replace manually or fetch dynamically
VARIABLE_IDS = {
    "cloud_water_swich": "7d2008e2-25d9-4a4b-9038-cbeb93b5672f",
    "dHT11tsensor": "9ee5a505-d461-480c-983b-a02449fe6ea8",
    "dHT11hsenso": "d426bf72-0a03-426b-8c43-7b32b99dc530",
    "capaitiveSoilMoistureSensor": "c54f0268-39b2-4334-a8aa-11f620107580",
    "water_valve": "8da7aae6-7f40-435c-ba7e-9c8a39d835bd",
    "waterStatusInt": "a800f920-4961-4853-85fb-43abbbaf303a"
}

def get_auth_token():
    print("🔑 Requesting access token...")
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": API_CREDENTIALS["client_id"],
        "client_secret": API_CREDENTIALS["client_secret"],
        "audience": API_CREDENTIALS["audience"]
    }

    try:
        response = requests.post(AUTH_URL, headers=headers, data=data)
        response.raise_for_status()
        return response.json()["access_token"]

    except requests.exceptions.HTTPError as http_err:
        print("❌ HTTP Error:")
        print(f"  Status Code: {response.status_code}")
        print(f"  Response: {response.text}")
        raise

    except Exception as err:
        print("❌ Unexpected error:", err)
        raise

def fetch_property_value(token, thing_id, variable_id):
    url = f"{THINGS_URL}/{thing_id}/properties/{variable_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        return res.json().get("last_value")
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error fetching variable {variable_id}: {e}")
        return None

def load_data():
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, "r") as f:
                return json.load(f)
        except Exception:
            print("⚠️ Failed to parse existing JSON. Creating new.")
    return {
        "garden_monitoring": {
            "device_info": {
                "name": "Arduino UNO R4 WiFi",
                "api_key_name": API_CREDENTIALS["name"],
                "api_key_created": API_CREDENTIALS["created_date"]
            },
            "readings": []
        }
    }

def save_data(data):
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Data saved to {JSON_FILE}")

def collect_sensor_data():
    print("\n📡 Starting garden data collection...")

    try:
        token = get_auth_token()
    except Exception:
        print("🛑 Failed to authenticate.")
        return

    if not THING_ID or THING_ID == "your-thing-id-here":
        print("⚠️ Please set the correct THING_ID in your script.")
        return

    data = load_data()
    reading = {
        "timestamp": datetime.now().isoformat(),
        "values": {}
    }

    for name, var_id in VARIABLE_IDS.items():
        value = fetch_property_value(token, THING_ID, var_id)
        reading["values"][name] = value
        print(f"📥 {name}: {value}")

    data["garden_monitoring"]["readings"].append(reading)
    save_data(data)

def run_periodically(interval_minutes=10):
    print(f"🕓 Collecting every {interval_minutes} minutes. Press Ctrl+C to stop.")
    try:
        while True:
            collect_sensor_data()
            time.sleep(interval_minutes * 60)
    except KeyboardInterrupt:
        print("\n🛑 Data collection stopped.")

if __name__ == "__main__":
    collect_sensor_data()
    # Uncomment below to run repeatedly
    # run_periodically(10)
