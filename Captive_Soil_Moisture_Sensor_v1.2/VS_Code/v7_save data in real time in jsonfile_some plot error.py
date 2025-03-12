import serial
import time
import matplotlib.pyplot as plt
import json
from datetime import datetime

# Replace 'COM3' with your actual COM port
ser = serial.Serial('COM3', 9600)

# Define the dry and wet values (calibrate these based on your sensor)
DRY_VALUE = 0    # Replace with your sensor's dry value
WET_VALUE = 1023 # Replace with your sensor's wet value

# Initialize lists to store time and sensor values
time_values = []
sensor_percentages = []

# Start the plot
plt.ion()
fig, ax = plt.subplots()
plot_line, = ax.plot(time_values, sensor_percentages, 'b-', label='Soil Moisture (%)')

# Set plot labels and title
ax.set_xlabel('Time')
ax.set_ylabel('Soil Moisture (%)')
ax.set_title('Real-time Soil Moisture Data Visualization')
ax.legend()

# Function to convert raw sensor value to percentage
def convert_to_percentage(raw_value):
    percentage = ((raw_value - DRY_VALUE) / (WET_VALUE - DRY_VALUE)) * 100
    return max(0, min(100, percentage))

# Initialize a list to store all data points
data_points = []

try:
    while True:
        if ser.in_waiting > 0:
            try:
                raw_data = ser.readline()
                print(f"Raw Data: {raw_data}")
                sensor_reading = raw_data.decode('utf-8').strip()
                soil_moisture_value = int(sensor_reading.split(': ')[1])

                # Convert the raw value to percentage
                soil_moisture_percentage = convert_to_percentage(soil_moisture_value)

                # Get current date and time
                now = datetime.now()
                date = now.strftime("%Y-%m-%d")
                current_time_formatted = now.strftime("%H:%M:%S")

                # Create a dictionary for the current data point
                data_point = {
                    "Date": date,
                    "Time": current_time_formatted,
                    "Soil Moisture (%)": soil_moisture_percentage
                }

                # Append the data point to the list
                data_points.append(data_point)

                # Write data to JSON file every second
                with open('soil_moisture_data.json', 'w') as json_file:
                    json.dump(data_points, json_file, indent=4)

                print(f'Date: {date}, Time: {current_time_formatted}, Soil Moisture: {soil_moisture_percentage:.2f}%')

            except (UnicodeDecodeError, ValueError, Exception) as e:
                print(f"Error processing data: {e}. Skipping this reading.")

        time.sleep(1)

except KeyboardInterrupt:
    print("Data collection stopped by the user.")
    ser.close()
    print("Serial connection closed.")
