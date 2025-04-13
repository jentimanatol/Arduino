const int sensorPin = 2;  // Pin connected to the sensor
volatile int pulseCount = 0;

void setup() {
  Serial.begin(9600);
  pinMode(sensorPin, INPUT);
  attachInterrupt(digitalPinToInterrupt(sensorPin), countPulses, RISING);
}

void loop() {
  delay(1000);  // Wait for 1 second
  Serial.print("Pulse count: ");
  Serial.println(pulseCount);
  pulseCount = 0;  // Reset the pulse count
}

void countPulses() {
  pulseCount++;
}
