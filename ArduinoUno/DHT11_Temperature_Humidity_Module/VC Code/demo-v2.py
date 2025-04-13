import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Change 'COM3' to your actual port (e.g., COM4, /dev/ttyUSB0, etc.)
ser = serial.Serial('COM3', 9600, timeout=1)

# Data storage lists
temperature_data = []
humidity_data = []

def update(frame):
    line = ser.readline().decode().strip()  # Read and decode serial data
    if line:
        try:
            temp, hum = map(float, line.split(","))  # Parse temperature & humidity
            temperature_data.append(temp)
            humidity_data.append(hum)

            # Keep only the last 50 readings to avoid clutter
            if len(temperature_data) > 50:
                temperature_data.pop(0)
                humidity_data.pop(0)

            ax1.clear()
            ax2.clear()

            ax1.plot(temperature_data, 'r-', label="Temperature (°C)")
            ax2.plot(humidity_data, 'b-', label="Humidity (%)")

            ax1.set_title("Real-time Temperature Data")
            ax2.set_title("Real-time Humidity Data")

            ax1.legend()
            ax2.legend()
        except ValueError:
            pass  # Ignore any parsing errors

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 6))
ani = animation.FuncAnimation(fig, update, interval=1000)

plt.show()
ser.close()
