# Sensores

Firmware en `firmware/`. HTTP primero. Contrato JSON: `docs/INGEST.md`.

| Sensor | Sketch | Notas |
|---|---|---|
| **Pluviómetro** (ToF VL53L1X + válvula + BME280) | `esp32_pluviometro_http` | **Primero en campo.** Toma. `docs/PLUVIOMETRO.md` |
| **DS18B20** | `esp32_ds18b20_http` | ±0.5 °C, cable largo, vaina. Pull-up 4.7 kΩ |
| **DHT22** | `esp32_dht22_http` (MQTT opcional) | Ambiente, no sumergible |
| **JSN-SR04T** | `esp32_tank_level_http` | Nivel tanque, domo que escurre CIP. No durante lavado |
| DHT11 | — | Tosco; no uses el sketch DHT22 tal cual |

## Punto de datos

```json
{"temperature": 22.4, "humidity": 67.0, "rssi": -58}
```

`humidity` solo si el hardware la tiene. `rssi` diagnostica Wi‑Fi.

Attributes (casi fijos): `source`, `hop`, `sensor`, `lote`, `site`.

## Red

ESP32 = Wi‑Fi **2.4 GHz**. Si no hay cobertura y **no** hay jaula de
Faraday: hop ESP-NOW (`docs/HOP.md`). Tanque metálico: no hop, cable o
domo. Un AP comercial solo cubre galpón; no es AAA.
