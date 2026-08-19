/*
 * data-logger — nivel de tanque (JSN-SR04T) store-and-forward → ThingsBoard.
 *
 * Ultrasónico en el DOMOS del techo, cara abajo. No medir durante CIP.
 * Buffer NVS: no se borra hasta POST 200.
 *
 * Ventanas de ordeño (hora local): 15 min dentro de [W1] y [W2].
 * Tras cada ventana: Wi-Fi y dump. Cada 6 h: una lectura de vigilancia.
 *
 * Pines default: TRIG GPIO 16, ECHO GPIO 17 (módulo 5 V: usar divisor en ECHO).
 * Copia ../secrets.h.example a secrets.h.
 */

#include <Preferences.h>
#include <time.h>
#include "secrets.h"
#include "../common/tb_wifi.h"
#include "../common/tb_http.h"

#ifndef TRIG_PIN
#define TRIG_PIN 16
#endif
#ifndef ECHO_PIN
#define ECHO_PIN 17
#endif
#ifndef TZ_OFFSET_S
#define TZ_OFFSET_S (-5 * 3600)
#endif
#ifndef TANK_EMPTY_MM
#define TANK_EMPTY_MM 2000.0f
#endif
#ifndef W1_START_H
#define W1_START_H 5
#endif
#ifndef W1_END_H
#define W1_END_H 7
#endif
#ifndef W2_START_H
#define W2_START_H 15
#endif
#ifndef W2_END_H
#define W2_END_H 17
#endif
#ifndef SAMPLE_EVERY_S
#define SAMPLE_EVERY_S 900
#endif
#ifndef WATCH_EVERY_S
#define WATCH_EVERY_S 21600
#endif
#ifndef CIP_START_H
#define CIP_START_H 7
#endif
#ifndef CIP_END_H
#define CIP_END_H 9
#endif

Preferences prefs;
uint32_t lastSample = 0;
uint32_t lastWatch = 0;
int lastDumpSlot = -1;

bool nowLocal(struct tm* t) {
  time_t n = time(nullptr);
  if (n < 1700000000) {
    return false;
  }
  localtime_r(&n, t);
  return true;
}

bool inRange(int h, int a, int b) { return h >= a && h < b; }

bool inMilking(const struct tm& t) {
  return inRange(t.tm_hour, W1_START_H, W1_END_H) || inRange(t.tm_hour, W2_START_H, W2_END_H);
}

bool inCip(const struct tm& t) { return inRange(t.tm_hour, CIP_START_H, CIP_END_H); }

int slotId(const struct tm& t) {
  return t.tm_yday * 10 + (inRange(t.tm_hour, W2_START_H, W2_END_H) ? 2 : 1);
}

float distanceMm() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(3);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(20);
  digitalWrite(TRIG_PIN, LOW);
  unsigned long us = pulseIn(ECHO_PIN, HIGH, 30000UL);
  if (us == 0) {
    return NAN;
  }
  return (float)us * 0.343f / 2.0f;
}

float levelMm() {
  float d = distanceMm();
  if (isnan(d)) {
    return NAN;
  }
  float h = TANK_EMPTY_MM - d;
  return h < 0 ? 0 : h;
}

String loadBuf() { return prefs.getString("buf", "[]"); }

void saveBuf(const String& s) { prefs.putString("buf", s); }

void pushSample(uint32_t tsMs, float level, const char* kind) {
  String buf = loadBuf();
  if (buf.length() > 3500) {
    Serial.println("buffer lleno: no añado hasta dump 200");
    return;
  }
  String item = "{\"ts\":" + String(tsMs) + ",\"values\":{";
  item += "\"level_mm\":" + String(level, 1) + ",";
  item += "\"kind\":\"";
  item += kind;
  item += "\"}}";
  if (buf == "[]") {
    buf = "[" + item + "]";
  } else {
    buf.remove(buf.length() - 1);
    buf += ",";
    buf += item;
    buf += "]";
  }
  saveBuf(buf);
  Serial.printf("buf + %s level=%.1f  n~%d\n", kind, level, buf.length());
}

bool dumpBuf() {
  String buf = loadBuf();
  if (buf == "[]" || buf.length() < 3) {
    return true;
  }
  tbConnectWifi(WIFI_SSID, WIFI_PASS);
  if (tbTelemetry(TB_HOST, TB_PORT, TB_TOKEN, buf)) {
    saveBuf("[]");
    Serial.println("dump OK, buffer vacío");
    return true;
  }
  Serial.println("dump FALLÓ — buffer intacto");
  return false;
}

void setup() {
  Serial.begin(115200);
  delay(200);
  Serial.println("data-logger  tank level HTTP (store-and-forward)");
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  prefs.begin("tank", false);
  tbConnectWifi(WIFI_SSID, WIFI_PASS);
  configTime(TZ_OFFSET_S, 0, "pool.ntp.org", "time.nist.gov");
  tbBootAttributes(TB_HOST, TB_PORT, TB_TOKEN, "tank_level");
}

void loop() {
  struct tm t;
  if (!nowLocal(&t)) {
    tbConnectWifi(WIFI_SSID, WIFI_PASS);
    delay(5000);
    return;
  }

  if (inCip(t)) {
    delay(5000);
    return;
  }

  uint32_t now = millis();
  bool milking = inMilking(t);

  if (milking && (lastSample == 0 || now - lastSample >= SAMPLE_EVERY_S * 1000UL)) {
    float lvl = levelMm();
    if (!isnan(lvl)) {
      pushSample((uint32_t)time(nullptr) * 1000UL, lvl, "ordeño");
    } else {
      Serial.println("JSN-SR04T: timeout. Revisa TRIG/ECHO y 5 V.");
    }
    lastSample = now;
  }

  if (!milking && lastDumpSlot != slotId(t)) {
    // Acabamos de salir de una ventana (hora == END).
    if (t.tm_hour == W1_END_H || t.tm_hour == W2_END_H) {
      dumpBuf();
      lastDumpSlot = slotId(t);
    }
  }

  if (lastWatch == 0 || now - lastWatch >= WATCH_EVERY_S * 1000UL) {
    if (!milking) {
      float lvl = levelMm();
      if (!isnan(lvl)) {
        pushSample((uint32_t)time(nullptr) * 1000UL, lvl, "watch");
        dumpBuf();
      }
      lastWatch = now;
    }
  }
  delay(2000);
}
