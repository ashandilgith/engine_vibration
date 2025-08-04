// --- hardware/esp32_sensor_code.ino (Regression Version) ---
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

// --- Variables for Simulating Conditions ---
long lastStateChange = 0;
int rpms[] = {800, 2500, 4000}; // Idle, Cruise, High
int sea_states[] = {0, 1, 2}; // Calm, Choppy, Stormy
int current_rpm = 800;
int current_sea_state = 0;
float current_fuel = 100.0;

void setup() {
  Serial.begin(115200);
  // Initialize sensors and connect to WiFi (full code in previous tutorials)
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  Serial.println("\nWiFi Connected");
  mpu.begin();
  sensors.begin();
  
  lastStateChange = millis();
  randomSeed(analogRead(0)); // Seed for random numbers
}

void loop() {
  // --- Simulate Changing Conditions every 15 seconds for varied data ---
  if (millis() - lastStateChange > 15000) {
    current_rpm = rpms[random(3)]; // Pick a random RPM state
    current_sea_state = sea_states[random(3)]; // Pick a random sea state
    current_fuel -= random(1, 5); // Simulate fuel consumption
    if (current_fuel < 10) { current_fuel = 100; } // Refuel
    
    lastStateChange = millis();
    Serial.println("--- SIMULATING NEW CONDITIONS ---");
  }

  if(WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    sensors_event_t a, g, temp_event;
    mpu.getEvent(&a, &g, &temp_event);
    sensors.requestTemperatures();
    float temperatureC = sensors.getTempCByIndex(0);

    // --- Create JSON payload with REAL and SIMULATED data ---
    String jsonPayload = "{";
    jsonPayload += "\"rpm\":" + String(current_rpm) + ",";
    // NOTE: We use the real sensor temp for 'ambient_temp_c' for this test
    jsonPayload += "\"ambient_temp_c\":" + String(temperatureC) + ","; 
    jsonPayload += "\"fuel_level_percent\":" + String(current_fuel) + ",";
    jsonPayload += "\"sea_state\":" + String(current_sea_state) + ",";
    // This is the actual, real vibration reading from the sensor
    jsonPayload += "\"az_vibration_actual\":" + String(a.acceleration.z); 
    jsonPayload += "}";

    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");
    http.POST(jsonPayload);
    http.end();
    
    Serial.println(jsonPayload);
  }
  delay(2000);
}
