# Prompt — dar de alta otra finca (customer)

---

En el ThingsBoard de `data-logger` (UI en http://127.0.0.1:8080,
tenant `tenant@thingsboard.org`) crea una finca nueva como Customer,
sin tocar las otras.

Nombre de la finca: NOMBRE_FINCA
Primer sensor: NOMBRE_SENSOR (tipo DHT22 o DS18B20), lote LOTE

1. Lee `docs/TENANTS.md` y `scripts/add_sensor.py`.
2. Usa la API (el helper `scripts/tb_client.py` o `add_sensor.py
   --customer "NOMBRE_FINCA"`) para crear el customer si no existe y
   registrar el dispositivo ahí.
3. Devuélveme: nombre del customer, device id, access token, URL HTTP
   de telemetría.
4. Explica en dos frases cómo el productor de esta finca verá solo sus
   dispositivos (user del customer) y qué no hay que construir.

No crees un tenant nuevo salvo que yo lo pida. Un Customer por finca
es el modelo del PoC.

---
