# Contrato de ingestión

Un origen = un Device de ThingsBoard = un access token.
MCU, laptop, Hermes y scripts usan el **mismo** HTTP:

```
POST http://HOST:8080/api/v1/$TOKEN/telemetry
Content-Type: application/json

{"temperature": 22.4, "humidity": 67.0, "rssi": -58}
```

MQTT equivalente: usuario = `$TOKEN`, contraseña vacía, tópico
`v1/devices/me/telemetry`.

No hay envelope propio. No hay AAA fuera de ThingsBoard.

## Telemetry (cambia a menudo)

| Clave | Quién |
|---|---|
| `temperature`, `humidity`, `rssi` | DHT / ambiente |
| `temperature` | DS18B20 |
| `rain_mm`, `level_mm`, `drain_ok` | pluviómetro |
| `level_mm`, `kind` | tanque (store-and-forward; puede ir en array con `ts`) |
| `fwd_ok`, `fwd_fail` | gateway ESP-NOW (telemetría del padre) |
| `battery_v` | solo si hay tap de celda + `BATTERY_ADC_PIN` |

Claves nuevas (`litros`, `ph`) se aceptan sin cambiar el servidor.

Lote con marca de tiempo (tanque):

```json
[{"ts": 1700000000000, "values": {"level_mm": 1200.5, "kind": "ordeño"}}]
```

## Attributes (casi fijos)

`source` (`esp32` \| `hermes` \| `script`), `hop` (`wifi` \| `espnow` \| `wired` \| `none`),
`sensor`, `firmware`, `lote`, `site`.

Registro:

```bash
python3 scripts/add_sensor.py --name X --sensor DHT22 --source esp32 --hop wifi
```

`--type` solo aplica al **crear**. `ensure_device` no muta un device existente.

Hermes: el attribute `source=hermes` identifica el origen. Un campo JSON
`source` dentro de la telemetría de un documento es otra cosa (tipo de
archivo); no los mezcles. Ver `hermes/README.md`.
