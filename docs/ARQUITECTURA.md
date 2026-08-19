# Arquitectura — qué es esto y qué no es

## Decisión

La plataforma **es ThingsBoard Community Edition**.
`data-logger` es el **puente**: no reimplementa un backend IoT. Empaqueta:

- el compose oficial (ThingsBoard 4.3.1.3 + PostgreSQL 18)
- scripts para crear customers, sensores y tokens
- firmware ESP32 (pluviómetro, temp, nivel de tanque, hop ESP-NOW)
- prompts para que un agente haga el despliegue

El Flask + AdminLTE que ocupaba este repo está retirado (`docs/LEGACY.md`).

## Planos

```
ESP32 / hop ESP-NOW / sensor virtual / (más adelante) Hermes
        |  HTTP :8080/api/v1/$TOKEN/telemetry
        |  MQTT :1883  v1/devices/me/telemetry
        v
 ThingsBoard CE  ← UI, dispositivos, dashboards, alarmas, tenants
        |
        v
 PostgreSQL (volumen Docker data-logger-tb-postgres-data)
```

## Quién hace qué

| Pieza | Responsabilidad |
|---|---|
| ThingsBoard CE | Dispositivos, tokens, telemetría, dashboards, alarmas, tenants/customers, usuarios |
| Este repo | Compose, bootstrap, firmware, prompts de agente |
| Hermes (otro repo, después) | Lee correos/PDFs/facturas y **inyecta** el resultado como telemetría HTTP al mismo ThingsBoard |
| AAA casero | No. Los permisos son tenants + customers + users de ThingsBoard |

## Flexibilidad

Un sensor nuevo no pide código de servidor. Se registra (UI o
`scripts/add_sensor.py`), se copia el token al ESP32 y se manda JSON:

```json
{"temperature": 22.4, "humidity": 67.0, "rssi": -58}
```

Claves nuevas (`litros`, `ph`, `peso`) aparecen solas en *Latest telemetry*.
ThingsBoard no exige un esquema fijo.

## Qué no entra aquí

- Parser de correo o PDF (Hermes).
- Backend Flask propio, ni login propio, ni base propia de usuarios.
- Trading, predicción, DOIN, OLAP de `predictor`.
- ThingsBoard Professional Edition. CE cubre el PoC y los primeros sitios.
  PE se evalúa solo si hace falta white-label o tenants aislados a escala.
- Un range extender como “AAA” o como solución de tanque metálico. Ver `docs/HOP.md`.

## Cuentas por defecto (solo con LOAD_DEMO)

| Rol | Correo | Clave |
|---|---|---|
| System admin | sysadmin@thingsboard.org | sysadmin |
| Tenant admin | tenant@thingsboard.org | tenant |
| Customer | customer@thingsboard.org | customer |

Cámbialas antes de abrir el puerto 8080 a una red.
