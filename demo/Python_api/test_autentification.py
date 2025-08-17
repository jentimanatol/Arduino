import requests
import json

# Arduino IoT Cloud API credentials
client_id = "Jr3t1Lgx5LIjDzPKCQ9Y8AUkI27RBjzv"
client_secret = "1OgQhAVeFXgwwvPRzJDyY1wE9p6kq3ssnmnXiPRZnd1S1JBnjFloWhqDbQkGkxZd"

# Arduino IoT Cloud API endpoints
auth_url = "https://api2.arduino.cc/iot/v2/oauth/token"

# Different format attempted with content-type header
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

# Try different parameter formats
data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret,
    "audience": "https://api2.arduino.cc/iot"
}

print("Attempting authentication with Arduino IoT Cloud...")
response = requests.post(auth_url, headers=headers, data=data)
print(f"Status code: {response.status_code}")
print(f"Response: {response.text}")

# Try alternative format without audience parameter
if response.status_code != 200:
    print("\nTrying alternative format...")
    alt_data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(auth_url, headers=headers, data=alt_data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")