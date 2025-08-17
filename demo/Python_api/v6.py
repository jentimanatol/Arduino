import requests
import json
import time

# Replace with your actual credentials and variable IDs
CLIENT_ID = "aICcKaGwfGI7QRrDtbkli8MQjzqGG1Y3"
CLIENT_SECRET = "GQQL6pukVfXwJyfTkR8OD69tQCzqFr9es9Exlke49Fv7psxOdDCPnDvWZjIXcBA0"
THING_ID = "a49ac818-fb0f-4320-9194-4d72d0a13765"
VARIABLE_IDS = {
    "cloud_water_swich": "7d2008e2-25d9-4a4b-9038-cbeb93b5672f",
    "dHT11tsensor": "9ee5a505-d461-480c-983b-a02449fe6ea8",
    "dHT11hsenso": "d426bf72-0a03-426b-8c43-7b32b99dc530",
    "capaitiveSoilMoistureSensor": "c54f0268-39b2-4334-a8aa-11f620107580",
    "water_valve": "8da7aae6-7f40-435c-ba7e-9c8a39d835bd",
    "waterStatusInt": "a800f920-4961-4853-85fb-43abbbaf303a"
}

# Define the API URL
API_URL = "https://api2.arduino.cc/iot/v2"

# Step 1: Request OAuth Token
def get_access_token():
    url = f"{API_URL}/oauth/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        token = response.json().get("access_token")
        print(f"Access token obtained: {token}")
        return token
    else:
        print(f"Failed to get access token: {response.status_code}")
        print(response.json())
        return None

# Step 2: Get Variable Data
def get_variable_data(access_token, variable_id):
    url = f"{API_URL}/things/{THING_ID}/variables/{variable_id}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error retrieving data for {variable_id}: {response.status_code}")
        print(response.json())
        return None

# Step 3: Collect and Display Data
def collect_sensor_data():
    print("📡 Starting garden data collection...")

    # Step 1: Get OAuth Token
    access_token = get_access_token()
    if not access_token:
        print("🛑 Failed to authenticate.")
        return
    
    while True:
        print("🔑 Requesting access token...")

        # Collect and print data from each variable
        for sensor, var_id in VARIABLE_IDS.items():
            print(f"🌿 Collecting data for {sensor}...")
            sensor_data = get_variable_data(access_token, var_id)
            
            if sensor_data:
                print(f"{sensor} - Value: {sensor_data['value']} {sensor_data.get('unit', '')}")
            else:
                print(f"Failed to retrieve data for {sensor}")

        print("\n🕑 Waiting for the next data collection cycle...")
        time.sleep(60)  # Collect data every 60 seconds

if __name__ == "__main__":
    collect_sensor_data()
