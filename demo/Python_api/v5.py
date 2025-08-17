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
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")
        return None
