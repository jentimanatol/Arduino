import serial
import time
import matplotlib.pyplot as plt
import json  # Import json module
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
ax.set_xlabel('Time (s)')
ax.set_ylabel('Soil Moisture (%)')
ax.set_title('Real-time Soil Moisture Data Visualization')
ax.legend()

# Set time tracking
start_time = time.time()

def convert_to_percentage(raw_value):
    # Convert raw sensor value to percentage
    percentage = ((raw_value - DRY_VALUE) / (WET_VALUE - DRY_VALUE)) * 100
    # Ensure the percentage is within 0-100 range
    return max(0, min(100, percentage))

# Initialize a list to store all data points
data_points = []

try:
    while True:
        # Read the sensor value from the serial port
        if ser.in_waiting > 0:
            try:
                # Read the raw data from the serial port
                raw_data = ser.readline()
                # Debug: Print the raw data
                print(f"Raw Data: {raw_data}")
                # Attempt to decode the data
                sensor_reading = raw_data.decode('utf-8').strip()
                # Extract the soil moisture value
                soil_moisture_value = int(sensor_reading.split(': ')[1])
                current_time = time.time() - start_time

                # Convert the raw value to percentage
                soil_moisture_percentage = convert_to_percentage(soil_moisture_value)

                # Append the values to the lists
                time_values.append(current_time)
                sensor_percentages.append(soil_moisture_percentage)

                # Update the plot
                plot_line.set_xdata(time_values)
                plot_line.set_ydata(sensor_percentages)
                ax.relim()
                ax.autoscale_view()
                fig.canvas.draw()
                fig.canvas.flush_events()

                # Get current date and time
                now = datetime.now()
                date = now.strftime("%Y-%m-%d")  # Format: YYYY-MM-DD
                current_time_formatted = now.strftime("%H:%M:%S")  # Format: HH:MM:SS

                # Create a dictionary for the current data point
                data_point = {
                    "Date": date,
                    "Time": current_time_formatted,
                    "Time (s)": current_time,
                    "Soil Moisture (%)": soil_moisture_percentage
                }

                # Append the data point to the list
                data_points.append(data_point)

                # Print the values to the console (for debugging purposes)
                print(f'Date: {date}, Time: {current_time_formatted}, Time (s): {current_time:.2f}, Soil Moisture: {soil_moisture_percentage:.2f}%')

            except UnicodeDecodeError:
                print("Error: Could not decode the data as UTF-8. Skipping this reading.")
            except ValueError:
                print("Error: Could not extract the soil moisture value. Skipping this reading.")
            except Exception as e:
                print(f"Unexpected error: {e}. Skipping this reading.")

        # Add a short delay to match the sensor reading rate
        time.sleep(1)

except KeyboardInterrupt:
    print("Data collection stopped by the user.")

finally:
    # Close the serial connection
    ser.close()

    # Save the data to a JSON file
    with open('soil_moisture_data.json', 'w') as json_file:
        json.dump(data_points, json_file, indent=4)  # Save with pretty-printing
    print("Data saved to 'soil_moisture_data.json'.")