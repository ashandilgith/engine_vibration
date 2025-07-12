// --- hardware/esp32_sensor_code.ino ---
#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// --- Configuration ---
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
String serverName = "https://your-codespace-url-5000.app.github.dev/data";
#define ONEWIRE_BUS 4

// --- Global Objects ---
Adafruit_MPU6050 mpu;
OneWire oneWire(ONEWIRE_BUS);
DallasTemperature sensors(&oneWire);

void connectToWiFi() { /* ... connection logic ... */ }
void setup() { /* ... sensor and wifi init ... */ }

void loop() {
  if(WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    sensors_event_t a, g, temp_event;
    mpu.getEvent(&a, &g, &temp_event);
    sensors.requestTemperatures();
    float temperatureC = sensors.getTempCByIndex(0);

    String jsonPayload = "{\"ax\":" + String(a.acceleration.x) + ",\"ay\":" + String(a.acceleration.y) + ",\"az\":" + String(a.acceleration.z) + ",\"gx\":" + String(g.gyro.x) + ",\"gy\":" + String(g.gyro.y) + ",\"gz\":" + String(g.gyro.z) + ",\"temperature_c\":" + String(temperatureC) + "}";

    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");
    http.POST(jsonPayload);
    http.end();
  }
  delay(2000);
}