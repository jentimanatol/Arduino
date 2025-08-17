import requests
import json
import time
from datetime import datetime
import os.path

# Arduino IoT Cloud API credentials
API_CREDENTIALS = {
    "name": "BhccGardenApiKeys",
    "created_date": "April 15, 2025",
    "client_id": "Jr3t1Lgx5LIjDzPKCQ9Y8AUkI27RBjzv",
    "client_secret": "1OgQhAVeFXgwwvPRzJDyY1wE9p6kq3ssnmnXiPRZnd1S1JBnjFloWhqDbQkGkxZd"
}

# Arduino IoT Cloud API endpoints
BASE_URL = "https://api2.arduino.cc/iot/v2"
AUTH_URL = f"{BASE_URL}/oauth/token"
DEVICES_URL = f"{BASE_URL}/devices"
PROPERTIES_URL = f"{BASE_URL}/things"

# JSON file to store data
JSON_FILE = "arduino_garden_data.json"

# Map of Arduino property IDs to their names from your code
PROPERTIES_MAP = {
    "cloud_water_swich": "Water Switch",
    "dHT11tsensor": "Temperature Sensor",
    "waterStatusInt": "Water Status", 
    "capaitiveSoilMoistureSensor": "Soil Moisture",
    "dHT11hsenso": "Air Humidity",
    "water_valve": "Water Valve"
}

def get_auth_token():
    """Get authentication token from Arduino IoT Cloud"""
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "grant_type": "client_credentials",
        "client_id": API_CREDENTIALS["client_id"],
        "client_secret": API_CREDENTIALS["client_secret"],
        "audience": "https://api2.arduino.cc/iot"
    }
    
    try:
        response = requests.post(AUTH_URL, headers=headers, data=data)
        response.raise_for_status()
        return response.json()["access_token"]
    except requests.exceptions.RequestException as e:
        print(f"Authentication error: {e}")
        return None

def get_devices(token):
    """Get list of devices from Arduino IoT Cloud"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(DEVICES_URL, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting devices: {e}")
        return []

def get_things(token):
    """Get list of things from Arduino IoT Cloud"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(PROPERTIES_URL, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting things: {e}")
        return []

def get_property_values(token, thing_id, property_ids):
    """Get property values for a specific thing"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    property_values = {}
    
    for prop_id in property_ids:
        try:
            response = requests.get(f"{PROPERTIES_URL}/{thing_id}/properties/{prop_id}", headers=headers)
            response.raise_for_status()
            property_values[prop_id] = response.json()["last_value"]
        except requests.exceptions.RequestException as e:
            print(f"Error getting property {prop_id}: {e}")
            property_values[prop_id] = None
    
    return property_values

def load_existing_data():
    """Load existing data from JSON file if it exists"""
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print(f"Error reading existing JSON file. Creating new file.")
    
    # Return a new data structure if file doesn't exist or is invalid
    return {
        "garden_monitoring": {
            "device_info": {
                "name": "Arduino Uno WiFi R4",
                "api_key_name": API_CREDENTIALS["name"],
                "api_key_created": API_CREDENTIALS["created_date"]
            },
            "readings": []
        }
    }

def save_data(data):
    """Save data to JSON file"""
    with open(JSON_FILE, 'w') as file:
        json.dump(data, file, indent=2)
    print(f"Data saved to {JSON_FILE}")

def collect_data():
    """Main function to collect data from Arduino and save to JSON"""
    # Get authentication token
    token = get_auth_token()
    if not token:
        print("Failed to authenticate. Check your API credentials.")
        return
    
    print("Authentication successful!")
    
    # Get devices and things
    devices = get_devices(token)
    things = get_things(token)
    
    if not devices or not things:
        print("No devices or things found. Check your Arduino IoT Cloud setup.")
        return
    
    print(f"Found {len(devices)} devices and {len(things)} things.")
    
    # Find the relevant device and thing for our garden monitoring
    device_id = None
    thing_id = None
    property_ids = []
    
    for device in devices:
        # Look for your Arduino Uno WiFi R4
        if "Arduino Uno WiFi" in device.get("name", ""):
            device_id = device["id"]
            break
    
    for thing in things:
        # Find thing associated with our device
        if thing.get("device_id") == device_id:
            thing_id = thing["id"]
            # Get all properties for this thing
            for prop in thing.get("properties", []):
                property_ids.append(prop["id"])
            break
    
    if not thing_id or not property_ids:
        print("Could not find matching thing or properties for your Arduino.")
        return
    
    # Get property values
    property_values = get_property_values(token, thing_id, property_ids)
    
    # Load existing data
    data = load_existing_data()
    
    # Create a new reading entry
    reading = {
        "timestamp": datetime.now().isoformat(),
        "values": {}
    }
    
    # Populate reading with sensor values
    for prop_id, value in property_values.items():
        # Map the property ID to a readable name if available
        name = PROPERTIES_MAP.get(prop_id, prop_id)
        reading["values"][name] = value
    
    # Add reading to data
    data["garden_monitoring"]["readings"].append(reading)
    
    # Save updated data
    save_data(data)
    print(f"Successfully collected data at {reading['timestamp']}")

def scheduled_collection(interval_minutes=10):
    """Run data collection on a schedule"""
    print(f"Starting scheduled data collection every {interval_minutes} minutes.")
    print("Press Ctrl+C to stop.")
    
    try:
        while True:
            print("\n--- Collecting data ---")
            collect_data()
            print(f"Waiting {interval_minutes} minutes until next collection...")
            time.sleep(interval_minutes * 60)
    except KeyboardInterrupt:
        print("\nData collection stopped.")

if __name__ == "__main__":
    # Collect data once
    collect_data()
    
    # Uncomment to run scheduled collection
    # scheduled_collection(10)  # Collect every 10 minutes