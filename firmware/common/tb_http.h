#pragma once
// POST a ThingsBoard Device API. Nunca imprime el token.

#include <WiFi.h>
#include <HTTPClient.h>

#ifndef FW_VERSION
#define FW_VERSION "1.0"
#endif
#ifndef HOP_MODE
#define HOP_MODE "wifi"
#endif
#ifndef SOURCE_NAME
#define SOURCE_NAME "esp32"
#endif

inline bool tbConnected() { return WiFi.status() == WL_CONNECTED; }

inline int tbPost(const char* host, int port, const char* token,
                  const char* resource, const String& body) {
  if (!tbConnected()) {
    return -1;
  }
  String url = String("http://") + host + ":" + String(port)
               + "/api/v1/" + token + "/" + resource;
  HTTPClient http;
  http.begin(url);
  http.addHeader("Content-Type", "application/json");
  int code = http.POST(body);
  http.end();
  Serial.printf("POST /api/v1/****/%s → %d  %s\n", resource, code, body.c_str());
  return code;
}

inline bool tbTelemetry(const char* host, int port, const char* token, const String& body) {
  return tbPost(host, port, token, "telemetry", body) == 200;
}

inline bool tbAttributes(const char* host, int port, const char* token, const String& body) {
  return tbPost(host, port, token, "attributes", body) == 200;
}

inline void tbBootAttributes(const char* host, int port, const char* token,
                             const char* sensor) {
  String body = "{";
  body += "\"source\":\"" SOURCE_NAME "\",";
  body += "\"hop\":\"" HOP_MODE "\",";
  body += "\"firmware\":\"" FW_VERSION "\",";
  body += "\"sensor\":\"";
  body += sensor;
  body += "\"}";
  tbAttributes(host, port, token, body);
}

#ifdef BATTERY_ADC_PIN
inline bool tbAppendBattery(String& body) {
  // Divisor en el tap de celda → ADC1 (GPIO 32–39). No leer el rail 5 V.
#ifndef BATTERY_DIVIDER
#define BATTERY_DIVIDER 2.0f
#endif
  float v = analogReadMilliVolts(BATTERY_ADC_PIN) / 1000.0f * BATTERY_DIVIDER;
  body += ",\"battery_v\":" + String(v, 3);
  return true;
}
#endif
