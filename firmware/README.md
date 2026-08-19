# Firmware ESP32

Repo: <https://github.com/harveybc/data-logger>  
Carpeta local: `/home/harveybc/Documents/GitHub/data-logger`

HTTP primero.
[Ingestión](https://github.com/harveybc/data-logger/blob/master/docs/INGEST.md) ·
[pluviómetro](https://github.com/harveybc/data-logger/blob/master/docs/PLUVIOMETRO.md) ·
[compras](https://github.com/harveybc/data-logger/blob/master/docs/BOM.md) ·
[hop](https://github.com/harveybc/data-logger/blob/master/docs/HOP.md)

| Carpeta | Qué | Cuándo |
|---|---|---|
| `esp32_tipping_bucket_http/` | Cubeta comercial (reed/pulso) | **Pedir esto en Amazon** |
| `esp32_pluviometro_http/` | ToF + válvula + BME280 | Plan B si ya tienes cubo/válvula |
| `esp32_dht22_http/` | DHT22 HTTP | Mesa / ambiente |
| `esp32_ds18b20_http/` | DS18B20 HTTP | Vaina / sombra |
| `esp32_tank_level_http/` | JSN-SR04T + buffer NVS | Nivel de tanque (domo CIP) |
| `esp32_espnow_node/` | Hijo ESP-NOW | Sombra RF **sin** Faraday |
| `esp32_gateway_http/` | Padre ESP-NOW → HTTP | Reenvía con el token del hijo |
| `esp32_dht22_mqtt/` | DHT22 MQTT | Opcional |
| `common/` | `tb_http.h`, `tb_wifi.h` | No se flashea solo |

Helpers: el Serial escribe `POST /api/v1/****/telemetry → code` (sin token).
Attributes `source` / `hop` / `firmware` / `sensor` al arrancar.

`USE_DEEP_SLEEP` y `INTERVAL_S 3600` solo en placa de Iq bajo (no DevKit,
no power bank). `BATTERY_ADC_PIN` solo con tap de celda a ADC1.

## Arduino IDE

1. [Arduino IDE 2](https://www.arduino.cc/en/software).
2. Boards URL: `https://espressif.github.io/arduino-esp32/package_esp32_index.json`.
3. Librerías según sketch: DHT + Unified Sensor; OneWire + DallasTemperature;
   VL53L1X (Pololu); Adafruit BME280; PubSubClient.

Placa: *ESP32 Dev Module* (mesa/mural) o FireBeetle si hay `USE_DEEP_SLEEP`.
115200 baud.

```bash
cp firmware/secrets.h.example firmware/esp32_pluviometro_http/secrets.h
python3 scripts/add_sensor.py --name pluviometro-01 --lote meteo --sensor pluviometro
```

`TB_HOST` = IP LAN de ThingsBoard, **nunca** `localhost`.

## Cableado corto

```
DHT22 / DS18B20 DATA → GPIO 4   (DS18B20: 4.7 kΩ a 3V3)
VL53L1X + BME280     → I2C 21/22
Válvula MOSFET       → GPIO 26
JSN-SR04T            → TRIG 16, ECHO 17 (divisor si el módulo es 5 V)
```

Éxito: Serial `→ 200` y *Latest telemetry* en la UI. 401 = token. Sin
Wi‑Fi = SSID o red 5 GHz (usa 2.4). `nan` = cableado.
