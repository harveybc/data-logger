/*
 * data-logger — pluviómetro comercial de cubeta basculante → ThingsBoard HTTP.
 *
 * El instrumento se vacía solo. Cada vuelco cierra un reed (pulso a GND).
 * rain_mm = tips * MM_PER_TIP  (típicamente 0.2 o 0.2794 mm).
 *
 * TIP_PIN con INPUT_PULLUP. Un lado del reed a GPIO, el otro a GND.
 * Debounce 50 ms. A las 00:00 local se reinicia el acumulado del día.
 *
 * Copia ../secrets.h.example a secrets.h.
 */

#include <time.h>
#include "secrets.h"
#include "../common/tb_wifi.h"
#include "../common/tb_http.h"

#ifndef TIP_PIN
#define TIP_PIN 27
#endif
#ifndef MM_PER_TIP
#define MM_PER_TIP 0.2f
#endif
#ifndef INTERVAL_S
#define INTERVAL_S 900
#endif
#ifndef TZ_OFFSET_S
#define TZ_OFFSET_S (-5 * 3600)
#endif
#ifndef DEBOUNCE_MS
#define DEBOUNCE_MS 50
#endif

volatile uint32_t tipsDay = 0;
volatile uint32_t tipsTotal = 0;
volatile uint32_t lastTipMs = 0;
int lastResetYday = -1;

void IRAM_ATTR onTip() {
  uint32_t now = millis();
  if (now - lastTipMs < DEBOUNCE_MS) {
    return;
  }
  lastTipMs = now;
  tipsDay++;
  tipsTotal++;
}

bool localTime(struct tm* out) {
  time_t n = time(nullptr);
  if (n < 1700000000) {
    return false;
  }
  localtime_r(&n, out);
  return true;
}

void resetAtMidnight() {
  struct tm t;
  if (!localTime(&t)) {
    return;
  }
  if (t.tm_hour == 0 && t.tm_min <= 2 && t.tm_yday != lastResetYday) {
    tipsDay = 0;
    lastResetYday = t.tm_yday;
    Serial.println("00:00  rain_mm del día a 0");
  }
}

void setup() {
  Serial.begin(115200);
  delay(200);
  Serial.println("data-logger  tipping bucket HTTP");
  pinMode(TIP_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(TIP_PIN), onTip, FALLING);
  tbConnectWifi(WIFI_SSID, WIFI_PASS);
  configTime(TZ_OFFSET_S, 0, "pool.ntp.org", "time.nist.gov");
  tbBootAttributes(TB_HOST, TB_PORT, TB_TOKEN, "pluviometro");
}

void loop() {
  tbConnectWifi(WIFI_SSID, WIFI_PASS);
  resetAtMidnight();
  noInterrupts();
  uint32_t day = tipsDay;
  uint32_t tot = tipsTotal;
  interrupts();
  float rain = day * MM_PER_TIP;
  String body = "{";
  body += "\"rain_mm\":" + String(rain, 2) + ",";
  body += "\"tips_day\":" + String(day) + ",";
  body += "\"tips_total\":" + String(tot) + ",";
  body += "\"rssi\":" + String(WiFi.RSSI());
  body += "}";
  tbTelemetry(TB_HOST, TB_PORT, TB_TOKEN, body);
  Serial.printf("rain_mm=%.2f  tips_day=%u\n", rain, day);
  delay((unsigned long)INTERVAL_S * 1000UL);
}
