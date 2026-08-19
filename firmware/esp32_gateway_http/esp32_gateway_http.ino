/*
 * data-logger — padre ESP-NOW → ThingsBoard HTTP.
 *
 * WIFI_AP_STA: se une al Wi-Fi del sitio (mismo canal que los hijos)
 * y reenvía cada paquete como POST /api/v1/$CHILD_TOKEN/telemetry.
 *
 * Emparejado hardcoded: CHILD_MAC_0 + CHILD_TOKEN_0 (hasta 4 hijos).
 * Si el AP cambia de canal, los hijos se caen. Fija el canal del AP.
 *
 * Este nodo NO es un range extender. No implementa AAA propio.
 * Copia secrets.h y rellena Wi-Fi, TB_HOST y los pares MAC/token.
 */

#include <WiFi.h>
#include <esp_now.h>
#include <esp_wifi.h>
#include "secrets.h"
#include "../common/tb_wifi.h"
#include "../common/tb_http.h"

#ifndef WIFI_CHANNEL
#define WIFI_CHANNEL 6
#endif
#ifndef GW_TOKEN
#define GW_TOKEN TB_TOKEN
#endif

typedef struct __attribute__((packed)) {
  uint8_t magic;
  char name[20];
  float temperature;
  float humidity;
  float extra;
  uint8_t flags;
} HopMsg;

struct Child {
  uint8_t mac[6];
  const char* token;
  const char* name;
};

Child children[4];
int nChildren = 0;
volatile uint32_t fwdOk = 0;
volatile uint32_t fwdFail = 0;

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

void addChild(const char* mac, const char* token, const char* name) {
  if (nChildren >= 4 || !mac || !token) {
    return;
  }
  if (!parseMac(mac, children[nChildren].mac)) {
    Serial.printf("MAC inválida: %s\n", mac);
    return;
  }
  children[nChildren].token = token;
  children[nChildren].name = name;
  nChildren++;
}

const Child* findChild(const uint8_t* mac) {
  for (int i = 0; i < nChildren; i++) {
    if (memcmp(children[i].mac, mac, 6) == 0) {
      return &children[i];
    }
  }
  return nullptr;
}

#if defined(ESP_ARDUINO_VERSION_MAJOR) && ESP_ARDUINO_VERSION_MAJOR >= 3
void onRecv(const esp_now_recv_info_t* info, const uint8_t* data, int len) {
  const uint8_t* mac = info->src_addr;
#else
void onRecv(const uint8_t* mac, const uint8_t* data, int len) {
#endif
  if (len < (int)sizeof(HopMsg)) {
    return;
  }
  HopMsg msg;
  memcpy(&msg, data, sizeof(msg));
  if (msg.magic != 0xD1) {
    return;
  }
  const Child* c = findChild(mac);
  if (!c) {
    Serial.printf("MAC desconocida %02X:%02X:%02X:%02X:%02X:%02X\n",
                  mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);
    fwdFail++;
    return;
  }
  String body = "{";
  if (msg.flags & 0x01) {
    body += "\"temperature\":" + String(msg.temperature, 2) + ",";
  }
  if (msg.flags & 0x02) {
    body += "\"humidity\":" + String(msg.humidity, 1) + ",";
  }
  body += "\"hop\":\"espnow\",";
  body += "\"rssi\":" + String(WiFi.RSSI());
  body += "}";
  bool ok = tbTelemetry(TB_HOST, TB_PORT, c->token, body);
  if (ok) {
    fwdOk++;
  } else {
    fwdFail++;
  }
}

void setup() {
  Serial.begin(115200);
  delay(200);
  Serial.println("data-logger  ESP-NOW gateway  (no es un repetidor Wi-Fi)");

#ifdef CHILD_MAC_0
  addChild(CHILD_MAC_0, CHILD_TOKEN_0, "child0");
#endif
#ifdef CHILD_MAC_1
  addChild(CHILD_MAC_1, CHILD_TOKEN_1, "child1");
#endif
#ifdef CHILD_MAC_2
  addChild(CHILD_MAC_2, CHILD_TOKEN_2, "child2");
#endif
#ifdef CHILD_MAC_3
  addChild(CHILD_MAC_3, CHILD_TOKEN_3, "child3");
#endif

  WiFi.mode(WIFI_AP_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  unsigned long start = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - start < 25000) {
    delay(400);
    Serial.print(".");
  }
  Serial.println();
  int ch = WiFi.channel();
  if (ch == 0) {
    ch = WIFI_CHANNEL;
  }
  esp_wifi_set_channel(ch, WIFI_SECOND_CHAN_NONE);
  Serial.printf("WiFi %s  canal=%d  fija este canal en el AP y en los hijos\n",
                WiFi.status() == WL_CONNECTED ? "OK" : "NO", ch);
  Serial.printf("padre MAC=%s  (ponla en GATEWAY_MAC del hijo)\n",
                WiFi.macAddress().c_str());

  if (esp_now_init() != ESP_OK) {
    Serial.println("esp_now_init FALLÓ");
    return;
  }
  esp_now_register_recv_cb(onRecv);
  tbBootAttributes(TB_HOST, TB_PORT, GW_TOKEN, "gateway");
}

void loop() {
  static uint32_t last = 0;
  if (millis() - last > 60000) {
    last = millis();
    String body = "{";
    body += "\"fwd_ok\":" + String(fwdOk) + ",";
    body += "\"fwd_fail\":" + String(fwdFail) + ",";
    body += "\"rssi\":" + String(WiFi.RSSI());
    body += "}";
    tbTelemetry(TB_HOST, TB_PORT, GW_TOKEN, body);
  }
  delay(200);
}
