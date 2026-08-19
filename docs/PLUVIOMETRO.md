# Pluviómetro 1A — prototipo de mesa primero

**Pedido recomendado:** cubeta basculante comercial (se vacía sola).
No hace falta ToF ni electroválvula. Ver
[BOM.md](https://github.com/harveybc/data-logger/blob/master/docs/BOM.md)
y el sketch `firmware/esp32_tipping_bucket_http/`.

Repo: <https://github.com/harveybc/data-logger>  
Compras (4 juegos): [BOM.md](https://github.com/harveybc/data-logger/blob/master/docs/BOM.md)  
Diseño: [DISENO.md](https://github.com/harveybc/data-logger/blob/master/docs/DISENO.md)

El **asistente de campo** (huecos, empaques, mangueras, conexiones a
intemperie) entra **después** de que el prototipo publique `rain_mm` en
ThingsBoard. En mesa: protoboard, USB y un cubo.

## Qué hace

1. Mide el nivel en un cubo de área conocida.
2. `rain_mm = level_mm * (A_cubo / A_embudo)`.
3. Cada 15 min manda `rain_mm`, `level_mm` (y BME280 si está).
4. A las **00:00** hora local: si hay agua, abre la electroválvula,
   espera nivel ≈ 0, cierra, `drain_ok=1`.

## Prototipo (tú)

- ESP32 por USB 5 V.
- Electroválvula con **MOSFET + diodo flyback** (GPIO 26). Nunca directo
  al pin del ESP32.
- Sensor de nivel: el que ya tengas (ver tabla en `BOM.md`). El sketch
  default es VL53L1X en I2C (GPIO 21/22).
- Mide `A_cubo`, `A_embudo` y `TOF_EMPTY_MM` (cubo seco) y ponlos en
  `secrets.h`.

```bash
cd data-logger
python3 scripts/add_sensor.py --name lluvia-01 --lote meteo --sensor pluviometro
cp firmware/secrets.h.example firmware/esp32_pluviometro_http/secrets.h
```

Arduino IDE: *ESP32 Dev Module*. Librerías: **VL53L1X** (Pololu),
**Adafruit BME280** (si lo usas). Sketch:
`firmware/esp32_pluviometro_http/`.

| Pin | Qué |
|---|---|
| 5 V USB / GND | ESP32 |
| GPIO 21 / 22 | I2C (VL53L1X y BME280) |
| GPIO 26 | gate del MOSFET (HIGH = abre válvula) |
| 12 V aparte | solo la bobina de la válvula |

Éxito: Serial `POST /api/v1/****/telemetry → 200` y *Latest telemetry*
con `rain_mm`.

## Montaje de intemperie (asistente de campo, después)

Una caja IP66, plástico, prensas abajo, pigtail 5 V, válvula al fondo,
ToF seco bajo la tapa. Lavado: manguera + jabón suave. Pasa de taller =
caja seca. El POST 200 lo confirma quien flasheó el prototipo.
