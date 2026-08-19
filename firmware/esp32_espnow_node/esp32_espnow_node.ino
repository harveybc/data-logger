/*
 * data-logger — hijo ESP-NOW (sombra RF sin Faraday).
 *
 * No habla ThingsBoard. Manda un paquete al MAC del padre.
 * El padre POSTea con el token del hijo.
 *
 * WiFi.mode(WIFI_STA) + canal FIJO (el mismo del AP del padre).
 * Si el AP cambia de canal, este hijo se cae.
 *
 * DHT22 en GPIO 4 por defecto. Copia secrets.h y pon GATEWAY_MAC.
 */

#include <WiFi.h>
#include <esp_now.h>
#include <esp_wifi.h>
#include <DHT.h>
#include "secrets.h"
#include "../common/tb_wifi.h"

#ifndef SENSOR_PIN
#define SENSOR_PIN 4
#endif
#ifndef INTERVAL_S
#define INTERVAL_S 3600
#endif
#ifndef WIFI_CHANNEL
#define WIFI_CHANNEL 6
#endif
#ifndef NODE_NAME
#define NODE_NAME "espnow-child"
#endif

#define DHTTYPE DHT22
DHT dht(SENSOR_PIN, DHTTYPE);

typedef struct __attribute__((packed)) {
  uint8_t magic;
  char name[20];
  float temperature;
  float humidity;
  float extra;
  uint8_t flags;
} HopMsg;

uint8_t gatewayMac[6];

bool parseMac(const char* s, uint8_t out[6]) {
  int b[6];
  if (sscanf(s, "%x:%x:%x:%x:%x:%x", &b[0], &b[1], &b[2], &b[3], &b[4], &b[5]) != 6) {
    return false;
  }
  for (int i = 0; i < 6; i++) {
    out[i] = (uint8_t)b[i];
  }
  return true;
}

void setup() {
  Serial.begin(115200);
  delay(200);
  Serial.println("data-logger  ESP-NOW child  (no es un repetidor Wi-Fi)");
  dht.begin();

  if (!parseMac(GATEWAY_MAC, gatewayMac)) {
    Serial.println("GATEWAY_MAC inválido (usa AA:BB:CC:DD:EE:FF)");
    return;
  }

  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  esp_wifi_set_channel(WIFI_CHANNEL, WIFI_SECOND_CHAN_NONE);
  if (esp_now_init() != ESP_OK) {
    Serial.println("esp_now_init FALLÓ");
    return;
  }
  esp_now_peer_info_t peer = {};
  memcpy(peer.peer_addr, gatewayMac, 6);
  peer.channel = WIFI_CHANNEL;
  peer.encrypt = false;
  esp_now_add_peer(&peer);
  Serial.printf("hijo MAC=%s  canal=%d\n", WiFi.macAddress().c_str(), WIFI_CHANNEL);
}

void loop() {
  HopMsg msg = {};
  msg.magic = 0xD1;
  strncpy(msg.name, NODE_NAME, sizeof(msg.name) - 1);
  float t = dht.readTemperature();
  float h = dht.readHumidity();
  if (isnan(t) || isnan(h)) {
    Serial.println("DHT22 inválido");
  } else {
    msg.temperature = t;
    msg.humidity = h;
    msg.flags = 0x03;
    esp_err_t e = esp_now_send(gatewayMac, (uint8_t*)&msg, sizeof(msg));
    Serial.printf("esp-now send t=%.2f h=%.1f  err=%d\n", t, h, (int)e);
  }
  tbWaitOrSleep(INTERVAL_S);
}
