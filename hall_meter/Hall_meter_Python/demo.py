import serial
import time

# Replace 'COM3' with the port name your Arduino is connected to
arduino_port = 'COM3'
baud_rate = 9600
timeout = 1

ser = serial.Serial(arduino_port, baud_rate, timeout=timeout)

def read_pulse_count():
    while True:
        if ser.in_waiting > 0:
            pulse_count = ser.readline().decode('utf-8').strip()
            print(f'Pulse count: {pulse_count}')
            consumption = calculate_consumption(int(pulse_count))
            print(f'Consumption: {consumption}')
            time.sleep(1)

def calculate_consumption(pulse_count):
    # Example calculation, adjust as needed for your specific use case
    return pulse_count * 0.1  # For example, if each pulse represents 0.1 unit of consumption

if __name__ == '__main__':
    read_pulse_count()
