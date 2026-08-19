# Sensores

## Temperatura (lo que Harvey va a desempolvar)

| Sensor | Qué mide | Precisión típica | Notas de finca |
|---|---|---|---|
| **DS18B20** | Temperatura | ±0.5 °C | Cable largo, se puede mojar (versión waterproof). Ideal establo, tanque, sombra. Resistencia 4.7 kΩ en DATA. |
| **DHT22 / AM2302** | Temp + humedad | ±0.5 °C / ±2–5 % HR | Barato, no sumergible. Bueno para ambiente (lechería, cuarto frío). |
| DHT11 | Temp + humedad | ±2 °C | Evítalo si puedes: es tosco. El sketch DHT22 no le sirve tal cual. |

Firmware listo en `firmware/`. HTTP primero, MQTT si quieres.

## Cómo se ve un punto de datos

```json
{
  "temperature": 22.4,
  "humidity": 67.0,
  "rssi": -58
}
```

`humidity` solo si el hardware la tiene. `rssi` ayuda a diagnosticar Wi‑Fi
malo en el galpón.

## Atributos (no cambian cada 30 s)

El bootstrap publica:

```json
{"finca": "Finca Demo", "lote": "establo-norte", "sensor": "DHT22"}
```

Sirven para filtrar dashboards (“todos los sensores del lote X”).

## Añadir otro tipo (pH, litros, peso)

No hay que tocar el servidor. En el JSON del ESP32 (o de Hermes) agregas
la clave. En la UI, *Latest telemetry* la muestra. Luego arrastras un
widget al dashboard.

## Red

El ESP32 habla **Wi‑Fi 2.4 GHz**. Si la finca no tiene Wi‑Fi en el
establo, opciones posteriores (no en este kit): ESP32 + LoRa hacia un
gateway, o un router 4G en la finca. El protocolo hacia ThingsBoard
sigue siendo HTTP o MQTT.
