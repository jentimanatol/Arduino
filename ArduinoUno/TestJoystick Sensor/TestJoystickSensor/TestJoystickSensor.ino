void setup() {
  Serial.begin(9600); // Start the serial communication at 9600 baud rate
}

void loop() {
  int sensorValue = analogRead(A0); // Read the value from the analog pin A0
  Serial.println(sensorValue);      // Print the value to the serial monitor
  delay(1000);                      // Wait for 1 second before the next reading
}
