/*
 * data-logger — ESP32 + DS18B20 → ThingsBoard por HTTP.
 *
 * Librerías (Arduino Library Manager):
 *   - OneWire
 *   - DallasTemperature
 *
 * Cableado DS18B20:
 *   VCC (rojo)   → 3V3
 *   GND (negro)  → GND
 *   DATA (amarillo) → GPIO 4  + resistencia 4.7 kΩ entre DATA y 3V3
 *
 * Copia ../secrets.h.example a secrets.h en esta carpeta y rellena WiFi + token.
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include "secrets.h"

#ifndef SENSOR_PIN
#define SENSOR_PIN 4
#endif
#ifndef INTERVAL_S
#define INTERVAL_S 30
#endif

OneWire oneWire(SENSOR_PIN);
DallasTemperature sensors(&oneWire);

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

bool sendTelemetry(float t) {
  if (WiFi.status() != WL_CONNECTED) {
    return false;
  }
  String url = String("http://") + TB_HOST + ":" + String(TB_PORT)
               + "/api/v1/" + TB_TOKEN + "/telemetry";
  String body = "{";
  body += "\"temperature\":" + String(t, 2) + ",";
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
  Serial.println("data-logger  ESP32 + DS18B20 + HTTP");
  sensors.begin();
  connectWifi();
}

void loop() {
  connectWifi();
  sensors.requestTemperatures();
  float t = sensors.getTempCByIndex(0);
  if (t == DEVICE_DISCONNECTED_C) {
    Serial.println("DS18B20: no hay sensor. Revisa DATA, GND, 3V3 y la resistencia de 4.7 kΩ.");
  } else {
    Serial.printf("t=%.2f C\n", t);
    sendTelemetry(t);
  }
  delay((unsigned long)INTERVAL_S * 1000UL);
}
