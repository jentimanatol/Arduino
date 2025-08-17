import requests
import time

# Replace these with your actual Arduino IoT Cloud credentials
CLIENT_ID = 'your_client_id_here'
CLIENT_SECRET = 'your_client_secret_here'

TOKEN_URL = "https://api2.arduino.cc/iot/v2/oauth/token"

def get_auth_token():
    print("🔑 Requesting access token...")

    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "audience": "https://api2.arduino.cc/iot"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(TOKEN_URL, data=payload, headers=headers)
        response.raise_for_status()
        token_data = response.json()
        print("✅ Access token received.")
        return token_data['access_token']
    except requests.exceptions.HTTPError as http_err:
        print("❌ HTTP Error:")
        print(f"  Status Code: {response.status_code}")
        print(f"  Response: {response.text}")
    except requests.exceptions.RequestException as req_err:
        print(f"❌ Request Error: {req_err}")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

    print("🛑 Failed to authenticate.")
    return None

def collect_sensor_data():
    print("📡 Starting garden data collection...")

    token = get_auth_token()
    if not token:
        return

    # Placeholder for your actual Thing ID
    thing_id = "a49ac818-fb0f-4320-9194-4d72d0a13765"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        # List all variables
        url = f"https://api2.arduino.cc/iot/v2/things/{thing_id}/properties"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        variables = response.json()

        print("\n🌱 Sensor Data:")
        for var in variables:
            name = var.get("name", "Unknown")
            last_value = var.get("last_value", "N/A")
            updated_at = var.get("updated_at", "N/A")
            print(f"  {name}: {last_value} (Last updated: {updated_at})")

    except requests.exceptions.HTTPError as http_err:
        print("❌ HTTP Error while fetching data:")
        print(f"  Status Code: {response.status_code}")
        print(f"  Response: {response.text}")
    except requests.exceptions.RequestException as req_err:
        print(f"❌ Request Error: {req_err}")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

# Run the script
if __name__ == "__main__":
    collect_sensor_data()
