{
  "devices": [
    {
      "name": "Arduino IoT Cloud Device",
      "id": "garden_monitoring_system",
      "sensors": [
        {
          "name": "DHT11 Temperature Sensor",
          "id": "dHT11tsensor",
          "type": "CloudTemperatureSensor",
          "value": 24.5,
          "unit": "Celsius",
          "readInterval": "10 seconds",
          "access": "READ"
        },
        {
          "name": "DHT11 Humidity Sensor",
          "id": "dHT11hsenso",
          "type": "CloudRelativeHumidity",
          "value": 65.2,
          "unit": "%",
          "readInterval": "10 seconds",
          "access": "READ"
        },
        {
          "name": "Capacitive Soil Moisture Sensor",
          "id": "capaitiveSoilMoistureSensor",
          "type": "CloudRelativeHumidity",
          "value": 42.8,
          "unit": "%",
          "readInterval": "10 seconds",
          "access": "READ"
        }
      ],
      "actuators": [
        {
          "name": "Water Switch",
          "id": "cloud_water_swich",
          "type": "CloudSwitch",
          "value": false,
          "access": "READWRITE",
          "onChange": "onCloudWaterSwichChange"
        },
        {
          "name": "Water Valve",
          "id": "water_valve",
          "type": "Boolean",
          "value": false,
          "access": "READ",
          "onChange": null
        }
      ],
      "status": [
        {
          "name": "Water Status",
          "id": "waterStatusInt",
          "type": "Integer",
          "value": 0,
          "access": "READ",
          "onChange": null
        }
      ],
      "network": {
        "ssid": "SECRET_SSID",
        "password": "SECRET_OPTIONAL_PASS",
        "connectionHandler": "WiFiConnectionHandler"
      }
    }
  ],
  "timestamp": "2025-04-22T14:30:00Z",
  "metadata": {
    "source": "Arduino IoT Cloud",
    "description": "Garden monitoring and watering system"
  }
}