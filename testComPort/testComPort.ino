void setup() {
    Serial.begin(9600); // Start serial communication at 9600 baud
}

void loop() {
    if (Serial.available() > 0) {
        String data = Serial.readString(); // Read the incoming data
        Serial.println(data); // Echo the data back to the serial port
    }
}
