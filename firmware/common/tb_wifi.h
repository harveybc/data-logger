#pragma once

#include <WiFi.h>

#ifdef USE_DEEP_SLEEP
#include <esp_sleep.h>
#endif

inline void tbConnectWifi(const char* ssid, const char* pass, uint32_t timeoutMs = 20000) {
  if (WiFi.status() == WL_CONNECTED) {
    return;
  }
  Serial.printf("WiFi: conectando a %s ...\n", ssid);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, pass);
  unsigned long start = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - start < timeoutMs) {
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

inline void tbWaitOrSleep(uint32_t intervalS) {
#ifdef USE_DEEP_SLEEP
  Serial.printf("deep sleep %u s (solo placa de Iq bajo; no DevKit ni power bank)\n", intervalS);
  Serial.flush();
  esp_sleep_enable_timer_wakeup((uint64_t)intervalS * 1000000ULL);
  esp_deep_sleep_start();
#else
  delay((unsigned long)intervalS * 1000UL);
#endif
}
