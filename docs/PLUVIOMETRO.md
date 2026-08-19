# Pluviómetro 1A — lo primero que se fabrica

Registro automático de lluvia para el veterinario (pastos). Sustituye la
lectura manual diaria. Una caja, toma de corriente, sin CIP, sin metal
alrededor.

Diseño largo: [`DISENO.md`](DISENO.md). Esta hoja es la de taller + flasheo.

## Qué hace

1. Mide el nivel de agua en un cubo de área conocida (ToF VL53L1X bajo la tapa).
2. Convierte a milímetros de lluvia: `rain_mm = level_mm * (A_cubo / A_embudo)`.
3. Cada 15 min manda `rain_mm`, `level_mm`, y si hay BME280 también
   `temperature`, `humidity`, `pressure`.
4. A las **00:00 hora local**: si hay agua, abre la electroválvula, espera
   a nivel ≈ 0, cierra, manda `drain_ok=1`.

Viento: no entra en este lote.

## Lugui (caja única)

- Caja IP66, interior mínimo **160 × 110 × 70 mm**, plástico (ABS/PC), no metal.
- Tapa de 4 tornillos, no potear. Taladros y prensas **abajo o de lado**.
- **PG9:** pigtail 5 V mural → JST-XH macho a la platina (no uses el USB
  de programación a la intemperie).
- **PG7:** cable de la electroválvula (fondo del cubo).
- Cubo de área conocida + embudo. ToF y BME280 **secos bajo la tapa**,
  mirando el agua (ToF) / el aire de la caja (BME).
- Válvula en el punto más bajo del cubo, con pendiente para que vacíe.
- Lavado: manguera + jabón suave. Pasa de taller = **caja seca por dentro**.
  El POST 200 lo confirma quien flashea, no el taller.

Escribir en etiqueta interior: `pluviometro-01`, `A_cubo` y `A_embudo` en mm².

## Flasheo

```bash
python3 scripts/add_sensor.py \
  --name pluviometro-01 --lote meteo --sensor pluviometro \
  --label "Lluvia diaria"
cp firmware/secrets.h.example firmware/esp32_pluviometro_http/secrets.h
# WIFI_*, TB_HOST, TB_TOKEN, A_CUBO_MM2, A_EMBUDO_MM2, TZ_OFFSET_S, TOF_EMPTY_MM
```

Arduino IDE: placa ESP32 Dev Module. Librerías: **VL53L1X** (Pololu),
**Adafruit BME280**, **Adafruit Unified Sensor**. Sketch:
`firmware/esp32_pluviometro_http/`.

| Pin | Qué |
|---|---|
| 3V3 / GND | VL53L1X y BME280 |
| GPIO 21 / 22 | I2C SDA / SCL |
| GPIO 26 | MOSFET de la válvula (activo en HIGH, diodo flyback en la bobina) |
| VIN | 5 V del pigtail |

Si no hay BME280 el sketch sigue (solo lluvia). Si no hay ToF, no publiques
`rain_mm` inventado: revisa el Serial.

## ThingsBoard

Device `pluviometro-01`. *Latest telemetry*: `rain_mm` (lo que mira el
veterinario), `level_mm`, `drain_ok`, y clima si hay BME.

Pendiente de medir en sitio (no bloquea fabricar la caja): área del cubo
y del embudo, voltaje de la válvula (5 V vs 12 V + fuente en la misma
caja), huso para las 00:00.
