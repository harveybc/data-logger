# Hop / gateway — no es un repetidor Wi‑Fi

Un range extender **no** autentica contra ThingsBoard, **no** habla
`/api/v1/$TOKEN/telemetry` y **no** saca radio de un tanque metálico.

| Situación | Qué usar |
|---|---|
| Sensor en / bajo metal (tanque) | Sonda o vaina por la pared; electrónica **fuera**. Nivel = domo en el techo. **No hop.** |
| Nodo ve Wi‑Fi 2.4 GHz | Sketch HTTP directo. Un AP comercial solo como cobertura. |
| Sombra RF **sin** Faraday (muro, loma) | Hijo ESP-NOW + padre Wi‑Fi (`esp32_espnow_node` + `esp32_gateway_http`) |
| Kilómetros / muchos aislados | LoRa más adelante. No es el lote 1. |

## Emparejado (lote 1C)

1. Registra el padre y cada hijo (tokens distintos):

```bash
python3 scripts/add_sensor.py --name gw-sombra-01 --sensor gateway --hop wifi
python3 scripts/add_sensor.py --name sombra-temp-01 --sensor DHT22 --hop espnow
```

2. Flashea el padre. El Serial imprime **su MAC** y el **canal** del AP.
3. Fija ese canal en el router (2.4 GHz, sin “auto”). Si el AP salta de
   canal, los hijos se caen.
4. En el hijo: `GATEWAY_MAC` = MAC del padre, `WIFI_CHANNEL` = ese canal.
5. En el padre: `CHILD_MAC_0` + `CHILD_TOKEN_0` (token del hijo).

El padre POSTea **como** el hijo. El hijo no lleva token de ThingsBoard.

Contrato en disco (no se commitea con tokens reales):
`secrets/gateway.json.example`.

## Qué no hacer

- Poner un TP-Link y decir que “ya hay AAA”.
- Meter el ESP32 dentro del tanque y “repetir” el Wi‑Fi.
- HMAC en ESP-NOW: aplazado (OQ 8 del diseño).
