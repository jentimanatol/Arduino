import requests
import json
import time
import matplotlib.pyplot as plt
from datetime import datetime

# Replace with your API credentials
CLIENT_ID = 'aICcKaGwfGI7QRrDtbkli8MQjzqGG1Y3'
CLIENT_SECRET = 'GQQL6pukVfXwJyfTkR8OD69tQCzqFr9es9Exlke49Fv7psxOdDCPnDvWZjIXcBA0'

# Arduino IoT Cloud API endpoints
BASE_URL = "https://api2.arduino.cc/iot/v2"
AUTH_URL = f"{BASE_URL}/oauth/token"
PROPERTIES_URL = f"{BASE_URL}/things/a49ac818-fb0f-4320-9194-4d72d0a13765/properties"

# Variable IDs
VARIABLE_IDS = {
    "cloud_water_swich": "7d2008e2-25d9-4a4b-9038-cbeb93b5672f",
    "dHT11tsensor": "9ee5a505-d461-480c-983b-a02449fe6ea8",
    "dHT11hsenso": "d426bf72-0a03-426b-8c43-7b32b99dc530",
    "capaitiveSoilMoistureSensor": "c54f0268-39b2-4334-a8aa-11f620107580",
    "water_valve": "8da7aae6-7f40-435c-ba7e-9c8a39d835bd",
    "waterStatusInt": "a800f920-4961-4853-85fb-43abbbaf303a"
}

# Data storage
sensor_data = {
    "timestamps": [],
    "temperature": [],
    "humidity": [],
    "soil_moisture": [],
    "water_status": [],
    "water_valve": [],
}

def get_auth_token():
    """Get authentication token from Arduino IoT Cloud"""
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "audience": "https://api2.arduino.cc/iot"
    }
    
    try:
        response = requests.post(AUTH_URL, headers=headers, data=data)
        response.raise_for_status()
        return response.json()["access_token"]
    except requests.exceptions.RequestException as e:
        print(f"Authentication error: {e}")
        return None

def get_property_value(token, variable_id):
    """Get property value for a specific variable ID"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{PROPERTIES_URL}/{variable_id}", headers=headers)
        response.raise_for_status()
        return response.json()["last_value"]
    except requests.exceptions.RequestException as e:
        print(f"Error getting property {variable_id}: {e}")
        return None

def collect_sensor_data():
    """Collect sensor data from the Arduino IoT Cloud"""
    # Get authentication token
    token = get_auth_token()
    if not token:
        print("Failed to authenticate. Check your API credentials.")
        return
    
    print("Authentication successful!")

    # Collect data for each variable
    timestamp = datetime.now().isoformat()
    sensor_data["timestamps"].append(timestamp)

    for variable_name, variable_id in VARIABLE_IDS.items():
        value = get_property_value(token, variable_id)
        if value is not None:
            sensor_data[variable_name].append(value)

    print(f"Data collected at {timestamp}")

def plot_data():
    """Plot the collected data using matplotlib"""
    if not sensor_data["timestamps"]:
        print("No data to visualize.")
        return

    # Plot temperature
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 2, 1)
    plt.plot(sensor_data["timestamps"], sensor_data["temperature"], label="Temperature (°C)", color="tab:blue")
    plt.xlabel("Timestamp")
    plt.ylabel("Temperature (°C)")
    plt.xticks(rotation=45)
    plt.title("Temperature Over Time")

    # Plot humidity
    plt.subplot(2, 2, 2)
    plt.plot(sensor_data["timestamps"], sensor_data["humidity"], label="Humidity (%)", color="tab:orange")
    plt.xlabel("Timestamp")
    plt.ylabel("Humidity (%)")
    plt.xticks(rotation=45)
    plt.title("Humidity Over Time")

    # Plot soil moisture
    plt.subplot(2, 2, 3)
    plt.plot(sensor_data["timestamps"], sensor_data["soil_moisture"], label="Soil Moisture (%)", color="tab:green")
    plt.xlabel("Timestamp")
    plt.ylabel("Soil Moisture (%)")
    plt.xticks(rotation=45)
    plt.title("Soil Moisture Over Time")

    # Plot water status
    plt.subplot(2, 2, 4)
    plt.plot(sensor_data["timestamps"], sensor_data["water_status"], label="Water Status", color="tab:red")
    plt.xlabel("Timestamp")
    plt.ylabel("Water Status (0 or 1)")
    plt.xticks(rotation=45)
    plt.title("Water Status Over Time")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Collect data periodically (you can adjust the number of cycles)
    print("Starting garden data collection...")
    for _ in range(5):  # Collect data 5 times
        collect_sensor_data()
        time.sleep(30)  # Wait for 30 seconds before next data collection

    # Plot the collected data
    plot_data()
