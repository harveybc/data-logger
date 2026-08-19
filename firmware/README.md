# Firmware ESP32 — temperatura de finca

Tres sketches listos. Empieza por HTTP: es el camino más corto para
comprobar que el ESP32 habla con ThingsBoard.

| Carpeta | Sensor | Protocolo | Cuándo usarlo |
|---|---|---|---|
| `esp32_dht22_http/` | DHT22 (temp + humedad) | HTTP POST | Primera prueba |
| `esp32_ds18b20_http/` | DS18B20 (solo temp, más preciso y mojable) | HTTP POST | Establo, tanque, sombra |
| `esp32_dht22_mqtt/` | DHT22 | MQTT 1883 | Cuando quieras menos overhead |

## Qué necesitas en el computador

1. [Arduino IDE 2](https://www.arduino.cc/en/software) (o PlatformIO).
2. Soporte ESP32: en IDE, *File → Preferences → Additional boards*, pega
   `https://espressif.github.io/arduino-esp32/package_esp32_index.json`,
   luego *Tools → Board → Boards Manager → esp32*.
3. Librerías (*Tools → Manage Libraries*):
   - DHT22: **DHT sensor library** (Adafruit) + **Adafruit Unified Sensor**
   - DS18B20: **OneWire** + **DallasTemperature**
   - MQTT: **PubSubClient**

Placa típica: *ESP32 Dev Module*, 115200 baud.

## Token y Wi‑Fi

```bash
cp firmware/secrets.h.example firmware/esp32_dht22_http/secrets.h
# edita WIFI_SSID, WIFI_PASS, TB_HOST, TB_TOKEN
```

`TB_HOST` es la IP LAN del computador donde corre ThingsBoard, **no**
`localhost`. En Linux:

```bash
hostname -I | awk '{print $1}'
```

El token lo imprime:

```bash
python3 scripts/bootstrap_finca.py          # sensores demo
python3 scripts/add_sensor.py --name pozo-temp-01 --lote pozo --sensor DS18B20
```

## Cableado

```
DHT22                         DS18B20
-----                         -------
VCC  → 3V3                    VCC (rojo)    → 3V3
GND  → GND                    GND (negro)   → GND
DATA → GPIO 4                 DATA (amarillo) → GPIO 4
                              + 4.7 kΩ entre DATA y 3V3
```

GPIO 4 se cambia con `#define SENSOR_PIN` en `secrets.h`.

## Cómo saber que funciona

1. Monitor serie a 115200: debe decir `WiFi OK` y `POST ... → 200`.
2. En ThingsBoard: *Entities → Devices → [tu sensor] → Latest telemetry*.
   En menos de un minuto aparecen `temperature` (y `humidity` si es DHT).

Si el POST da **401**, el token está mal. Si no hay Wi‑Fi, SSID/clave o
banda 5 GHz (usa la red 2.4 GHz). Si el sensor lee `nan`, es cableado.

## HTTP vs MQTT

HTTP basta para temperatura cada 30 s. MQTT (`esp32_dht22_mqtt`) usa el
mismo token como usuario MQTT, contraseña vacía, tópico
`v1/devices/me/telemetry`, puerto 1883. El ESP32 y el servidor tienen
que verse en la misma LAN (o el 1883 tiene que estar publicado).
