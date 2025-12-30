#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

// ====== Wi-Fi credentials ======
const char* ssid = "Oppo A78 5G";
const char* password = "akszayan";

// ====== Static IP configuration ======
IPAddress local_IP(10, 188, 183, 155);   // ESP32 IP
IPAddress gateway(10, 188, 183, 13);     // Gateway
IPAddress subnet(255, 255, 255, 0);

// ====== FastAPI backend URL ======
const char* serverUrl = "http://10.188.183.234:8000/iot_data";

// ====== Buzzer Pin ======
#define BUZZER_PIN 5

void setup() {
  Serial.begin(115200);

  // Buzzer setup
  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(BUZZER_PIN, LOW);

  // Configure Static IP
  if (!WiFi.config(local_IP, gateway, subnet)) {
    Serial.println("⚠️ Failed to configure Static IP");
  }

  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✅ WiFi Connected!");
  Serial.print("ESP32 IP Address: ");
  Serial.println(WiFi.localIP());

  // Init MPU6050
  Wire.begin();
  mpu.initialize();

  // Wake up MPU6050 (disable sleep mode)
  Wire.beginTransmission(0x68);
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);     // set to zero (wakes up MPU6050)
  Wire.endTransmission(true);

  if (mpu.testConnection()) {
    Serial.println("✅ MPU6050 connected");
  } else {
    Serial.println("❌ MPU6050 connection failed");
  }
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    int16_t ax, ay, az;
    int16_t gx, gy, gz;
    mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

    // Convert raw accel to g (±2g → 16384 LSB/g)
    float accelX = ax / 16384.0;
    float accelY = ay / 16384.0;
    float accelZ = az / 16384.0;

    // Convert raw gyro to °/s (±250°/s → 131 LSB/°/s)
    float gyroX = gx / 131.0;
    float gyroY = gy / 131.0;
    float gyroZ = gz / 131.0;

    // Debug print
    Serial.print("Accel[g] X:");
    Serial.print(accelX, 2);
    Serial.print(" Y:");
    Serial.print(accelY, 2);
    Serial.print(" Z:");
    Serial.println(accelZ, 2);

    Serial.print("Gyro[°/s] X:");
    Serial.print(gyroX, 2);
    Serial.print(" Y:");
    Serial.print(gyroY, 2);
    Serial.print(" Z:");
    Serial.println(gyroZ, 2);

    // Build JSON payload
    String payload = "{";
    payload += "\"accel_x\":" + String(accelX, 2) + ",";
    payload += "\"accel_y\":" + String(accelY, 2) + ",";
    payload += "\"accel_z\":" + String(accelZ, 2) + ",";
    payload += "\"gyro_x\":" + String(gyroX, 2) + ",";
    payload += "\"gyro_y\":" + String(gyroY, 2) + ",";
    payload += "\"gyro_z\":" + String(gyroZ, 2);
    payload += "}";

    Serial.println("📤 Sending: " + payload);

    // Send HTTP POST
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(payload);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("📥 Response: " + response);

      if (response.indexOf("\"alert\":true") > 0 || response.indexOf("\"force_buzzer\":true") > 0) {
        Serial.println("⚠️ ALERT or FORCE! Buzzing...");
        digitalWrite(BUZZER_PIN, HIGH);
        delay(5000);
        digitalWrite(BUZZER_PIN, LOW);
      }
    } else {
      Serial.print("❌ Error sending: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  } else {
    Serial.println("🔄 WiFi disconnected, reconnecting...");
    WiFi.begin(ssid, password);
  }

  delay(2000);
}
