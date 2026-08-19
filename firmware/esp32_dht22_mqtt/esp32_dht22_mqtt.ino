/*
 * data-logger — ESP32 + DHT22 → ThingsBoard por MQTT.
 *
 * Librerías:
 *   - DHT sensor library (Adafruit)
 *   - Adafruit Unified Sensor
 *   - PubSubClient (Nick O'Leary)
 *
 * MQTT: usuario = TB_TOKEN, contraseña vacía, tópico v1/devices/me/telemetry
 *
 * Copia ../secrets.h.example a secrets.h en esta carpeta.
 */

#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include "secrets.h"

#ifndef SENSOR_PIN
#define SENSOR_PIN 4
#endif
#ifndef INTERVAL_S
#define INTERVAL_S 30
#endif
#ifndef TB_MQTT_PORT
#define TB_MQTT_PORT 1883
#endif

#define DHTTYPE DHT22
DHT dht(SENSOR_PIN, DHTTYPE);

WiFiClient wifi;
PubSubClient mqtt(wifi);

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
  }
}

void connectMqtt() {
  if (mqtt.connected()) {
    return;
  }
  mqtt.setServer(TB_HOST, TB_MQTT_PORT);
  String clientId = String("esp32-") + String((uint32_t)ESP.getEfuseMac(), HEX);
  Serial.printf("MQTT: conectando a %s:%d como %s ...\n", TB_HOST, TB_MQTT_PORT, clientId.c_str());
  if (mqtt.connect(clientId.c_str(), TB_TOKEN, "")) {
    Serial.println("MQTT OK");
  } else {
    Serial.printf("MQTT FALLÓ  state=%d\n", mqtt.state());
  }
}

void setup() {
  Serial.begin(115200);
  delay(200);
  Serial.println("data-logger  ESP32 + DHT22 + MQTT");
  dht.begin();
  connectWifi();
  connectMqtt();
}

void loop() {
  connectWifi();
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
    Serial.printf("pub %s  ok=%d\n", body, ok);
  }
  delay((unsigned long)INTERVAL_S * 1000UL);
}
