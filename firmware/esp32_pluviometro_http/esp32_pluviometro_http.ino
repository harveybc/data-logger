/*
 * data-logger — pluviómetro de acumulación → ThingsBoard HTTP.
 *
 * VL53L1X (I2C) = nivel. BME280 (I2C, opcional) = T/HR/P.
 * GPIO 26 = MOSFET de electroválvula. A las 00:00 local drena si hay agua.
 *
 * Librerías: VL53L1X (Pololu), Adafruit BME280, Adafruit Unified Sensor.
 * Copia ../secrets.h.example a secrets.h en esta carpeta.
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <time.h>
#include <VL53L1X.h>
#include <Adafruit_BME280.h>
#include "secrets.h"

#ifndef INTERVAL_S
#define INTERVAL_S 900
#endif
#ifndef VALVE_PIN
#define VALVE_PIN 26
#endif
#ifndef VALVE_OPEN_S
#define VALVE_OPEN_S 25
#endif
#ifndef EMPTY_LEVEL_MM
#define EMPTY_LEVEL_MM 3.0f
#endif
#ifndef A_CUBO_MM2
#define A_CUBO_MM2 10000.0f
#endif
#ifndef A_EMBUDO_MM2
#define A_EMBUDO_MM2 10000.0f
#endif
#ifndef TZ_OFFSET_S
#define TZ_OFFSET_S (-5 * 3600)
#endif
#ifndef TOF_EMPTY_MM
#define TOF_EMPTY_MM 200.0f
#endif

VL53L1X tof;
Adafruit_BME280 bme;
bool haveTof = false;
bool haveBme = false;
int lastDrainYday = -1;

void connectWifi() {
  if (WiFi.status() == WL_CONNECTED) {
    return;
  }
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  unsigned long start = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - start < 20000) {
    delay(400);
  }
}

bool sendTelemetry(const String& body) {
  if (WiFi.status() != WL_CONNECTED) {
    return false;
  }
  String url = String("http://") + TB_HOST + ":" + String(TB_PORT)
               + "/api/v1/" + TB_TOKEN + "/telemetry";
  HTTPClient http;
  http.begin(url);
  http.addHeader("Content-Type", "application/json");
  int code = http.POST(body);
  Serial.printf("POST /api/v1/****/telemetry → %d  %s\n", code, body.c_str());
  http.end();
  return code == 200;
}

bool sendAttributes() {
  if (WiFi.status() != WL_CONNECTED) {
    return false;
  }
  String url = String("http://") + TB_HOST + ":" + String(TB_PORT)
               + "/api/v1/" + TB_TOKEN + "/attributes";
  String body = "{\"source\":\"esp32\",\"hop\":\"wifi\",\"sensor\":\"pluviometro\"}";
  HTTPClient http;
  http.begin(url);
  http.addHeader("Content-Type", "application/json");
  int code = http.POST(body);
  http.end();
  return code == 200;
}

// ToF mira hacia abajo: cubo vacío = distancia grande (TOF_EMPTY_MM).
// Columna de agua = vacío − lectura actual.
float levelMm() {
  if (!haveTof) {
    return NAN;
  }
  uint16_t d = tof.read();
  if (tof.timeoutOccurred() || d == 0) {
    return NAN;
  }
  float height = TOF_EMPTY_MM - (float)d;
  if (height < 0) {
    height = 0;
  }
  return height;
}

float rainMm(float level) {
  if (isnan(level) || A_EMBUDO_MM2 <= 0) {
    return NAN;
  }
  return level * (A_CUBO_MM2 / A_EMBUDO_MM2);
}

String telemetryBody(float level, float rain, int drainOk) {
  String body = "{";
  if (!isnan(level)) {
    body += "\"level_mm\":" + String(level, 1) + ",";
  }
  if (!isnan(rain)) {
    body += "\"rain_mm\":" + String(rain, 2) + ",";
  }
  if (haveBme) {
    body += "\"temperature\":" + String(bme.readTemperature(), 2) + ",";
    body += "\"humidity\":" + String(bme.readHumidity(), 1) + ",";
    body += "\"pressure\":" + String(bme.readPressure() / 100.0f, 1) + ",";
  }
  body += "\"rssi\":" + String(WiFi.RSSI()) + ",";
  body += "\"drain_ok\":" + String(drainOk);
  body += "}";
  return body;
}

bool localTime(struct tm* out) {
  time_t now = time(nullptr);
  if (now < 1700000000) {
    return false;
  }
  localtime_r(&now, out);
  return true;
}

void drainIfMidnight() {
  struct tm t;
  if (!localTime(&t)) {
    return;
  }
  if (t.tm_hour != 0 || t.tm_min > 2) {
    return;
  }
  if (t.tm_yday == lastDrainYday) {
    return;
  }
  float level = levelMm();
  int ok = 0;
  if (!isnan(level) && level > EMPTY_LEVEL_MM) {
    Serial.println("00:00  abriendo válvula");
    digitalWrite(VALVE_PIN, HIGH);
    delay((unsigned long)VALVE_OPEN_S * 1000UL);
    digitalWrite(VALVE_PIN, LOW);
    delay(2000);
    float after = levelMm();
    ok = (!isnan(after) && after <= EMPTY_LEVEL_MM) ? 1 : 0;
    sendTelemetry(telemetryBody(after, rainMm(after), ok));
  } else {
    ok = 1;
    sendTelemetry(telemetryBody(level, rainMm(level), ok));
  }
  lastDrainYday = t.tm_yday;
  Serial.printf("drenaje drain_ok=%d\n", ok);
}

void setup() {
  Serial.begin(115200);
  delay(200);
  Serial.println("data-logger  pluviometro HTTP");
  pinMode(VALVE_PIN, OUTPUT);
  digitalWrite(VALVE_PIN, LOW);

  Wire.begin(21, 22);
  tof.setTimeout(80);
  haveTof = tof.init();
  if (haveTof) {
    tof.setDistanceMode(VL53L1X::Short);
    tof.startContinuous(200);
    Serial.println("VL53L1X OK");
  } else {
    Serial.println("VL53L1X AUSENTE — no publiques rain_mm hasta que esté");
  }
  haveBme = bme.begin(0x76) || bme.begin(0x77);
  Serial.println(haveBme ? "BME280 OK" : "BME280 ausente (ok)");

  connectWifi();
  configTime(TZ_OFFSET_S, 0, "pool.ntp.org", "time.nist.gov");
  sendAttributes();
}

void loop() {
  connectWifi();
  drainIfMidnight();
  float level = levelMm();
  float rain = rainMm(level);
  sendTelemetry(telemetryBody(level, rain, 0));
  delay((unsigned long)INTERVAL_S * 1000UL);
}
