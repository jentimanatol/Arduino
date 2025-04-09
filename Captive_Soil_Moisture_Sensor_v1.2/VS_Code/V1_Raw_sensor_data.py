import serial
import time
import matplotlib.pyplot as plt

# Replace 'COM3' with your actual COM port
ser = serial.Serial('COM3', 9600)

# Initialize lists to store time and sensor values
time_values = []
sensor_values = []

# Start the plot
plt.ion()
fig, ax = plt.subplots()
plot_line, = ax.plot(time_values, sensor_values, 'b-', label='Soil Moisture')

# Set plot labels and title
ax.set_xlabel('Time (s)')
ax.set_ylabel('Soil Moisture Value')
ax.set_title('Real-time Soil Moisture Data Visualization')
ax.legend()

# Set time tracking
start_time = time.time()

try:
    while True:
        # Read the sensor value from the serial port
        if ser.in_waiting > 0:
            sensor_reading = ser.readline().decode('utf-8').strip()
            soil_moisture_value = int(sensor_reading.split(': ')[1])
            current_time = time.time() - start_time

            # Append the values to the lists
            time_values.append(current_time)
            sensor_values.append(soil_moisture_value)

            # Update the plot
            plot_line.set_xdata(time_values)
            plot_line.set_ydata(sensor_values)
            ax.relim()
            ax.autoscale_view()
            fig.canvas.draw()
            fig.canvas.flush_events()

            # Print the values to the console (for debugging purposes)
            print(f'Time: {current_time:.2f} s, Soil Moisture: {soil_moisture_value}')

        # Add a short delay to match the sensor reading rate
        time.sleep(1)

except KeyboardInterrupt:
    print("Data collection stopped by the user.")

finally:
    # Close the serial connection
    ser.close()
