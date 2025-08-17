import requests
import json
import time
from datetime import datetime
import os.path

# Arduino IoT Cloud API credentials
API_CREDENTIALS = {
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
    "cloud_water_swich": {"name": "Water Switch", "unit": ""},
    "dHT11tsensor": {"name": "Temperature Sensor", "unit": "°C"},
    "waterStatusInt": {"name": "Water Status", "unit": ""}, 
    "capaitiveSoilMoistureSensor": {"name": "Soil Moisture", "unit": "%"},
    "dHT11hsenso": {"name": "Air Humidity", "unit": "%"},
    "water_valve": {"name": "Water Valve", "unit": ""}
}

def get_auth_token():
    """Get authentication token from Arduino IoT Cloud with detailed error handling"""
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "grant_type": "client_credentials",
        "client_id": API_CREDENTIALS["client_id"],
        "client_secret": API_CREDENTIALS["client_secret"],
        "audience": "https://api2.arduino.cc/iot"
    }
    
    print("Attempting authentication with Arduino IoT Cloud...")
    
    try:
        response = requests.post(AUTH_URL, headers=headers, data=data)
        
        # Print diagnostic information
        print(f"Status code: {response.status_code}")
        
        # Handle specific status codes
        if response.status_code == 401:
            print("ERROR: Authentication failed (401 Unauthorized)")
            print("Possible issues:")
            print("  - Client ID or Client Secret may be incorrect")
            print("  - API key may not be activated")
            print("  - API key may not have the required permissions")
            print("\nAPI Response:", response.text)
            return None
            
        elif response.status_code == 403:
            print("ERROR: Authentication forbidden (403 Forbidden)")
            print("This usually means your API key doesn't have permission to access this endpoint")
            print("\nAPI Response:", response.text)
            return None
            
        elif response.status_code == 400:
            print("ERROR: Bad request (400)")
            print("There might be a formatting issue with the authentication request")
            print("\nAPI Response:", response.text)
            return None
            
        elif response.status_code >= 500:
            print(f"ERROR: Server error ({response.status_code})")
            print("The Arduino IoT Cloud server might be experiencing issues")
            print("\nAPI Response:", response.text)
            return None
            
        response.raise_for_status()
        token_data = response.json()
        
        if "access_token" not in token_data:
            print("ERROR: Authentication response doesn't contain an access token")
            print("Response:", token_data)
            return None
            
        print("Authentication successful! Token received.")
        return token_data["access_token"]
        
    except requests.exceptions.ConnectionError:
        print("ERROR: Failed to connect to Arduino IoT Cloud API")
        print("Please check your internet connection and try again")
        return None
        
    except json.JSONDecodeError:
        print("ERROR: Received invalid JSON response from authentication endpoint")
        print("Raw response:", response.text)
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Authentication request failed: {e}")
        return None

def get_devices(token):
    """Get list of devices from Arduino IoT Cloud"""
    if not token:
        print("No authentication token available")
        return []
        
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        print("Requesting devices list...")
        response = requests.get(DEVICES_URL, headers=headers)
        
        if response.status_code != 200:
            print(f"ERROR: Failed to get devices (Status code: {response.status_code})")
            print("Response:", response.text)
            return []
            
        devices = response.json()
        print(f"Found {len(devices)} devices")
        return devices
        
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Failed to get devices: {e}")
        return []

def get_things(token):
    """Get list of things from Arduino IoT Cloud"""
    if not token:
        print("No authentication token available")
        return []
        
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        print("Requesting things list...")
        response = requests.get(PROPERTIES_URL, headers=headers)
        
        if response.status_code != 200:
            print(f"ERROR: Failed to get things (Status code: {response.status_code})")
            print("Response:", response.text)
            return []
            
        things = response.json()
        print(f"Found {len(things)} things")
        return things
        
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Failed to get things: {e}")
        return []

def get_property_values(token, thing_id, properties):
    """Get property values for a specific thing"""
    if not token:
        print("No authentication token available")
        return {}
        
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    property_values = {}
    
    print(f"Fetching property values for thing {thing_id}...")
    for prop in properties:
        prop_id = prop.get("id", "")
        prop_name = prop.get("name", prop_id)
        
        try:
            print(f"  Fetching property: {prop_name} (ID: {prop_id})")
            url = f"{PROPERTIES_URL}/{thing_id}/properties/{prop_id}"
            response = requests.get(url, headers=headers)
            
            if response.status_code != 200:
                print(f"    ERROR: Failed to get property (Status: {response.status_code})")
                continue
                
            prop_data = response.json()
            last_value = prop_data.get("last_value")
            property_values[prop_id] = {
                "name": prop_name,
                "value": last_value,
                "variable_name": prop.get("variable_name", ""),
                "type": prop.get("type", "")
            }
            print(f"    Value: {last_value}")
            
        except requests.exceptions.RequestException as e:
            print(f"    ERROR: Request failed: {e}")
        except json.JSONDecodeError:
            print(f"    ERROR: Invalid JSON response")
            
    return property_values

def load_existing_data():
    """Load existing data from JSON file if it exists"""
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, 'r') as file:
                print(f"Loading existing data from {JSON_FILE}")
                return json.load(file)
        except json.JSONDecodeError:
            print(f"Error reading existing JSON file. Creating new file.")
    else:
        print(f"No existing data file found. Will create {JSON_FILE}")
    
    # Return a new data structure if file doesn't exist or is invalid
    return {
        "garden_monitoring": {
            "device_info": {
                "name": "Arduino Uno WiFi R4",
                "api_key_created": "April 15, 2025"
            },
            "readings": []
        }
    }

def save_data(data):
    """Save data to JSON file"""
    try:
        with open(JSON_FILE, 'w') as file:
            json.dump(data, file, indent=2)
        print(f"Data successfully saved to {JSON_FILE}")
    except Exception as e:
        print(f"ERROR: Failed to save data: {e}")

def format_property_value(prop_id, value, prop_type):
    """Format property value based on its type"""
    if prop_type == "TEMPERATURE":
        return f"{value:.1f}°C" if value is not None else "N/A"
    elif prop_type == "HUMIDITY":
        return f"{value:.1f}%" if value is not None else "N/A"
    elif prop_type == "SWITCH":
        return "ON" if value else "OFF"
    elif prop_type == "STATUS":
        return str(value) if value is not None else "N/A"
    else:
        return value

def print_current_values(properties):
    """Print current values in a readable format"""
    print("\n=== CURRENT SENSOR READINGS ===")
    for prop_id, prop_data in properties.items():
        name = PROPERTIES_MAP.get(prop_id, {}).get("name", prop_id)
        unit = PROPERTIES_MAP.get(prop_id, {}).get("unit", "")
        value = prop_data.get("value")
        prop_type = prop_data.get("type", "")
        
        formatted_value = format_property_value(prop_id, value, prop_type)
        print(f"{name}: {formatted_value}{' ' + unit if value is not None and unit else ''}")
    print("==============================\n")

def collect_data():
    """Main function to collect data from Arduino and save to JSON"""
    print("=" * 50)
    print(f"Arduino IoT Cloud Data Logger - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Get authentication token
    token = get_auth_token()
    if not token:
        print("Authentication failed. Cannot proceed.")
        return False
    
    # Get devices and things
    devices = get_devices(token)
    things = get_things(token)
    
    if not devices:
        print("No devices found. Check your Arduino IoT Cloud setup.")
        return False
    
    if not things:
        print("No things found. Check your Arduino IoT Cloud setup.")
        return False
    
    # Find Arduino Uno WiFi R4 device and associated thing
    device_id = None
    device_name = None
    
    print("\nLooking for Arduino Uno WiFi R4...")
    for device in devices:
        name = device.get("name", "")
        print(f"  Device: {name} (ID: {device.get('id', 'unknown')})")
        
        # Look for Arduino Uno WiFi R4 or any Arduino device if specific one not found
        if "arduino uno wifi" in name.lower():
            device_id = device.get("id")
            device_name = name
            print(f"  Found target device: {name}")
            break
    
    # If no specific device found, use first available Arduino device
    if not device_id:
        for device in devices:
            name = device.get("name", "")
            if "arduino" in name.lower():
                device_id = device.get("id")
                device_name = name
                print(f"  Using first available Arduino device: {name}")
                break
    
    if not device_id:
        print("Could not find any Arduino device. Please check your Arduino IoT Cloud account.")
        return False
    
    # Find thing associated with the device
    thing_id = None
    thing_name = None
    thing_properties = []
    
    print("\nLooking for thing associated with device...")
    for thing in things:
        if thing.get("device_id") == device_id:
            thing_id = thing.get("id")
            thing_name = thing.get("name", "Unknown Thing")
            thing_properties = thing.get("properties", [])
            print(f"  Found thing: {thing_name} (ID: {thing_id})")
            print(f"  This thing has {len(thing_properties)} properties")
            break
    
    if not thing_id:
        print("Could not find any thing associated with the selected device.")
        return False
    
    # Get property values
    property_values = get_property_values(token, thing_id, thing_properties)
    
    if not property_values:
        print("No property values found. Check your Arduino IoT Cloud setup.")
        return False
    
    # Print current values
    print_current_values(property_values)
    
    # Load existing data
    data = load_existing_data()
    
    # Create a new reading entry
    reading = {
        "timestamp": datetime.now().isoformat(),
        "values": {}
    }
    
    # Populate reading with sensor values
    for prop_id, prop_data in property_values.items():
        prop_name = PROPERTIES_MAP.get(prop_id, {}).get("name", prop_id)
        reading["values"][prop_name] = prop_data.get("value")
    
    # Add reading to data
    data["garden_monitoring"]["readings"].append(reading)
    
    # Update device info
    data["garden_monitoring"]["device_info"]["name"] = device_name
    
    # Save updated data
    save_data(data)
    
    print(f"Successfully collected data at {reading['timestamp']}")
    return True

def scheduled_collection(interval_minutes=10):
    """Run data collection on a schedule"""
    print(f"Starting scheduled data collection every {interval_minutes} minutes.")
    print("Press Ctrl+C to stop.")
    
    try:
        while True:
            success = collect_data()
            next_collection = datetime.now().replace(microsecond=0) + \
                             timedelta(minutes=interval_minutes)
            
            if success:
                print(f"\nNext collection scheduled for: {next_collection}")
            else:
                print(f"\nCollection failed. Will retry at: {next_collection}")
            
            # Wait until next collection time
            print(f"Waiting {interval_minutes} minutes until next collection...")
            time.sleep(interval_minutes * 60)
    except KeyboardInterrupt:
        print("\nData collection stopped by user.")

def check_auth_only():
    """Function to only test authentication"""
    print("Testing Arduino IoT Cloud authentication only...")
    token = get_auth_token()
    
    if token:
        print("\nAUTHENTICATION SUCCESSFUL")
        print("Your API credentials are working correctly")
        return True
    else:
        print("\nAUTHENTICATION FAILED")
        print("Please check your API credentials and try again")
        return False

if __name__ == "__main__":
    print("""
Arduino IoT Cloud Data Logger
============================
1. Test authentication only
2. Collect data once
3. Run scheduled collection (every 10 minutes)
    """)
    
    try:
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            check_auth_only()
        elif choice == '2':
            collect_data()
        elif choice == '3':
            interval = input("Enter collection interval in minutes (default: 10): ").strip()
            interval = int(interval) if interval.isdigit() else 10
            scheduled_collection(interval)
        else:
            print("Invalid choice. Please run the script again.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")