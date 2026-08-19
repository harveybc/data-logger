/*
 * data-logger — ESP32 + DHT22 → ThingsBoard por MQTT.
 *
 * Librerías: DHT + Adafruit Unified Sensor + PubSubClient.
 * Usuario MQTT = TB_TOKEN, contraseña vacía.
 * Sin deep sleep (reabrir :1883 + sleep es otro PR).
 */

#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include "secrets.h"
#include "../common/tb_wifi.h"

#ifndef SENSOR_PIN
#define SENSOR_PIN 4
#endif
#ifndef INTERVAL_S
#define INTERVAL_S 30
#endif
#ifndef TB_MQTT_PORT
#define TB_MQTT_PORT 1883
#endif
#ifndef FW_VERSION
#define FW_VERSION "1.0"
#endif
#ifndef HOP_MODE
#define HOP_MODE "wifi"
#endif

#define DHTTYPE DHT22
DHT dht(SENSOR_PIN, DHTTYPE);
WiFiClient wifi;
PubSubClient mqtt(wifi);

void connectMqtt() {
  if (mqtt.connected()) {
    return;
  }
  mqtt.setServer(TB_HOST, TB_MQTT_PORT);
  String clientId = String("esp32-") + String((uint32_t)ESP.getEfuseMac(), HEX);
  Serial.printf("MQTT: conectando a %s:%d ...\n", TB_HOST, TB_MQTT_PORT);
  if (mqtt.connect(clientId.c_str(), TB_TOKEN, "")) {
    Serial.println("MQTT OK");
    mqtt.publish("v1/devices/me/attributes",
                 "{\"source\":\"esp32\",\"hop\":\"" HOP_MODE "\",\"firmware\":\"" FW_VERSION "\",\"sensor\":\"DHT22\"}");
  } else {
    Serial.printf("MQTT FALLÓ  state=%d\n", mqtt.state());
  }
}

void setup() {
  Serial.begin(115200);
  delay(200);
  Serial.println("data-logger  ESP32 + DHT22 + MQTT");
  dht.begin();
  tbConnectWifi(WIFI_SSID, WIFI_PASS);
  connectMqtt();
}

void loop() {
  tbConnectWifi(WIFI_SSID, WIFI_PASS);
  connectMqtt();
  mqtt.loop();

  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if (isnan(h) || isnan(t)) {
    Serial.println("DHT22: lectura inválida.");
  } else {
    char body[96];
    snprintf(body, sizeof(body),
             "{\"temperature\":%.2f,\"humidity\":%.1f,\"rssi\":%d}",
             t, h, WiFi.RSSI());
    bool ok = mqtt.publish("v1/devices/me/telemetry", body);
    Serial.printf("pub telemetry ok=%d  %s\n", ok, body);
  }
  delay((unsigned long)INTERVAL_S * 1000UL);
}
