import serial
import time
import json
import os
from datetime import datetime

# Replace 'COM3' with your actual COM port
ser = serial.Serial('COM3', 9600)

# JSON file path
file_path = 'soil_moisture_data.json'

# Load existing data if file exists
if os.path.exists(file_path) and os.stat(file_path).st_size > 0:
    with open(file_path, 'r') as json_file:
        try:
            data_points = json.load(json_file)
        except json.JSONDecodeError:
            data_points = []
else:
    data_points = []

try:
    while True:
        if ser.in_waiting > 0:
            raw_data = ser.readline()
            sensor_reading = raw_data.decode('utf-8').strip()
            soil_moisture_value = int(sensor_reading.split(': ')[1])
            
            now = datetime.now()
            date = now.strftime("%Y-%m-%d")
            current_time_formatted = now.strftime("%H:%M:%S")
            
            data_point = {
                "Date": date,
                "Time": current_time_formatted,
                "Soil Moisture (%)": soil_moisture_value
            }
            
            data_points.append(data_point)
            
            with open(file_path, 'w') as json_file:
                json.dump(data_points, json_file, indent=4)
            
            print(f'Date: {date}, Time: {current_time_formatted}, Soil Moisture: {soil_moisture_value}%')
        
        time.sleep(1)

except KeyboardInterrupt:
    print("Data collection stopped by the user.")
    ser.close()
