#include <DHT.h>

#define DHTPIN 4         // Connect DATA pin to Digital Pin 2
#define DHTTYPE DHT11    // Define sensor type

DHT dht(DHTPIN, DHTTYPE);

void setup() {
    Serial.begin(9600);
    dht.begin();
}

void loop() {
    float temperature = dht.readTemperature();  // Read temperature (Celsius)
    float humidity = dht.readHumidity();       // Read humidity

    // Check if the readings are valid
    if (isnan(temperature) || isnan(humidity)) {
        Serial.println("Error reading from DHT sensor!");
    } else {
        Serial.print(temperature);
        Serial.print(",");
        Serial.println(humidity);
    }

    delay(2000);  // Delay for 2 seconds
}
