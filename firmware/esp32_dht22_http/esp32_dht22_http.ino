/*
 * data-logger — ESP32 + DHT22 → ThingsBoard por HTTP.
 *
 * Librerías: DHT sensor library (Adafruit) + Adafruit Unified Sensor.
 * Copia ../secrets.h.example a secrets.h.
 *
 * USE_DEEP_SLEEP solo en placa de Iq bajo (no DevKit, no power bank).
 * BATTERY_ADC_PIN solo con tap de celda a ADC1 (GPIO 32–39).
 */

#include <DHT.h>
#include "secrets.h"
#include "../common/tb_wifi.h"
#include "../common/tb_http.h"

#ifndef SENSOR_PIN
#define SENSOR_PIN 4
#endif
#ifndef INTERVAL_S
#define INTERVAL_S 30
#endif

#define DHTTYPE DHT22
DHT dht(SENSOR_PIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  delay(200);
  Serial.println("data-logger  ESP32 + DHT22 + HTTP");
  dht.begin();
  tbConnectWifi(WIFI_SSID, WIFI_PASS);
  tbBootAttributes(TB_HOST, TB_PORT, TB_TOKEN, "DHT22");
}

void loop() {
  tbConnectWifi(WIFI_SSID, WIFI_PASS);
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if (isnan(h) || isnan(t)) {
    Serial.println("DHT22: lectura inválida. Revisa cableado y SENSOR_PIN.");
  } else {
    Serial.printf("t=%.2f C  h=%.1f %%\n", t, h);
    String body = "{";
    body += "\"temperature\":" + String(t, 2) + ",";
    body += "\"humidity\":" + String(h, 1) + ",";
    body += "\"rssi\":" + String(WiFi.RSSI());
#ifdef BATTERY_ADC_PIN
    tbAppendBattery(body);
#endif
    body += "}";
    tbTelemetry(TB_HOST, TB_PORT, TB_TOKEN, body);
  }
  tbWaitOrSleep(INTERVAL_S);
}
