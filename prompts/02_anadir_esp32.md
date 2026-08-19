# Prompt — registrar un ESP32 de temperatura

Copia el recuadro. Rellena las tres líneas de MAYÚSCULAS antes de
pegárselo al agente.

---

Necesito añadir un sensor de temperatura ESP32 a la finca que ya corre
en este repo (`data-logger`).

Datos del sensor:
- Nombre del dispositivo: NOMBRE_UNICO (ejemplo: establo-sur-temp-01)
- Lote / lugar: LOTE (ejemplo: establo-sur)
- Tipo de sensor: DHT22 o DS18B20
- ThingsBoard ya está arriba en TB_URL (si no lo sabes, usa
  http://127.0.0.1:8080)

Haz exactamente esto:

1. Lee `firmware/README.md` y `scripts/add_sensor.py`.
2. Corre
   `python3 scripts/add_sensor.py --name NOMBRE_UNICO --lote LOTE --sensor TIPO`.
3. Muéstrame el access token y la URL HTTP de telemetría.
4. Crea `firmware/esp32_XXX_http/secrets.h` a partir de
   `firmware/secrets.h.example` dejando WIFI_SSID / WIFI_PASS como
   placeholders para que yo los escriba. Pon en `TB_HOST` la IP LAN de
   esta máquina (`hostname -I`) y en `TB_TOKEN` el token nuevo.
5. Dime qué sketch abrir en Arduino IDE, qué librerías instalar, cómo
   va el cableado (GPIO 4) y cómo compruebo en la UI que llegaron
   `temperature` (y `humidity` si es DHT).

No implementes un servidor nuevo. No uses localhost como TB_HOST del
ESP32.

---
