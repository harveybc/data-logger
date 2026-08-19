/*
 * data-logger — ESP32 + DS18B20 → ThingsBoard por HTTP.
 *
 * Librerías: OneWire + DallasTemperature.
 * DATA GPIO 4 + 4.7 kΩ a 3V3. Copia ../secrets.h.example a secrets.h.
 */

#include <OneWire.h>
#include <DallasTemperature.h>
#include "secrets.h"
#include "../common/tb_wifi.h"
#include "../common/tb_http.h"

#ifndef SENSOR_PIN
#define SENSOR_PIN 4
#endif
#ifndef INTERVAL_S
#define INTERVAL_S 30
#endif

OneWire oneWire(SENSOR_PIN);
DallasTemperature sensors(&oneWire);

void setup() {
  Serial.begin(115200);
  delay(200);
  Serial.println("data-logger  ESP32 + DS18B20 + HTTP");
  sensors.begin();
  tbConnectWifi(WIFI_SSID, WIFI_PASS);
  tbBootAttributes(TB_HOST, TB_PORT, TB_TOKEN, "DS18B20");
}

void loop() {
  tbConnectWifi(WIFI_SSID, WIFI_PASS);
  sensors.requestTemperatures();
  float t = sensors.getTempCByIndex(0);
  if (t == DEVICE_DISCONNECTED_C) {
    Serial.println("DS18B20: no hay sensor. Revisa DATA, GND, 3V3 y 4.7 kΩ.");
  } else {
    Serial.printf("t=%.2f C\n", t);
    String body = "{";
    body += "\"temperature\":" + String(t, 2) + ",";
    body += "\"rssi\":" + String(WiFi.RSSI());
#ifdef BATTERY_ADC_PIN
    tbAppendBattery(body);
#endif
    body += "}";
    tbTelemetry(TB_HOST, TB_PORT, TB_TOKEN, body);
  }
  tbWaitOrSleep(INTERVAL_S);
}
