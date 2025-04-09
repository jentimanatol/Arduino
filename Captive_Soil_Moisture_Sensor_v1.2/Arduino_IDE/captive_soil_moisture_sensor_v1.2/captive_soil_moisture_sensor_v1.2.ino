// Include the necessary libraries
#include <Arduino.h>

// Define the pin for the soil moisture sensor
const int soilMoisturePin = A0;

// Variable to store the sensor value
int soilMoistureValue = 0;

void setup() {
  // Initialize the serial communication
  Serial.begin(9600);
}

void loop() {
  // Read the analog value from the soil moisture sensor
  soilMoistureValue = analogRead(soilMoisturePin);

  // Print the sensor value to the Serial Monitor
  Serial.print("Soil Moisture Value: ");
  Serial.println(soilMoistureValue);

  // Add a short delay before the next reading
  delay(1000);
}
