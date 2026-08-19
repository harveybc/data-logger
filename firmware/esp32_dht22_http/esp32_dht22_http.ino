/*
 * data-logger — ESP32 + DHT22 → ThingsBoard por HTTP.
 *
 * Librerías (Arduino Library Manager):
 *   - DHT sensor library (Adafruit)
 *   - Adafruit Unified Sensor
 *
 * Cableado DHT22:
 *   VCC  → 3V3
 *   GND  → GND
 *   DATA → GPIO 4  (y, si tu módulo no lo trae, 10 kΩ entre DATA y 3V3)
 *
 * Copia ../secrets.h.example a secrets.h en esta carpeta y rellena WiFi + token.
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include "secrets.h"

#ifndef SENSOR_PIN
#define SENSOR_PIN 4
#endif
#ifndef INTERVAL_S
#define INTERVAL_S 30
#endif

#define DHTTYPE DHT22
DHT dht(SENSOR_PIN, DHTTYPE);

void connectWifi() {
  if (WiFi.status() == WL_CONNECTED) {
    return;
  }
  Serial.printf("WiFi: conectando a %s ...\n", WIFI_SSID);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  unsigned long start = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - start < 20000) {
    delay(400);
    Serial.print(".");
  }
  Serial.println();
  if (WiFi.status() == WL_CONNECTED) {
    Serial.print("WiFi OK  IP=");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("WiFi FALLÓ. Reintento en el próximo ciclo.");
  }
}

bool sendTelemetry(float t, float h) {
  if (WiFi.status() != WL_CONNECTED) {
    return false;
  }
  String url = String("http://") + TB_HOST + ":" + String(TB_PORT)
               + "/api/v1/" + TB_TOKEN + "/telemetry";
  String body = "{";
  body += "\"temperature\":" + String(t, 2) + ",";
  body += "\"humidity\":" + String(h, 1) + ",";
  body += "\"rssi\":" + String(WiFi.RSSI());
  body += "}";

  HTTPClient http;
  http.begin(url);
  http.addHeader("Content-Type", "application/json");
  int code = http.POST(body);
  Serial.printf("POST %s  → %d  %s\n", url.c_str(), code, body.c_str());
  http.end();
  return code == 200;
}

void setup() {
  Serial.begin(115200);
  delay(200);
  Serial.println("data-logger  ESP32 + DHT22 + HTTP");
  dht.begin();
  connectWifi();
}

void loop() {
  connectWifi();
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if (isnan(h) || isnan(t)) {
    Serial.println("DHT22: lectura inválida. Revisa cableado y SENSOR_PIN.");
  } else {
    Serial.printf("t=%.2f C  h=%.1f %%\n", t, h);
    sendTelemetry(t, h);
  }
  delay((unsigned long)INTERVAL_S * 1000UL);
}
