# Prompt — el sensor no aparece / no manda datos

---

El sensor NOMBRE no muestra telemetría en ThingsBoard. Diagnostica con
el kit `data-logger`. No reinstales desde cero y no borres volúmenes.

1. Lee `AGENTS.md` (sección Do not touch) y corre `bash scripts/diagnose.sh`.
2. Comprueba, en este orden:
   - `docker compose ps` — `thingsboard-ce` healthy / running
   - `curl` a `/login` en el puerto de `.env` (`TB_HTTP_PORT`, default 8080)
   - que `secrets/devices.json` o `secrets/NOMBRE.json` existe y el token
     coincide con *Entities → Devices → Manage credentials*
   - un POST de prueba: `python3 scripts/send_demo_telemetry.py --once`
     (o un `curl` al `/api/v1/$TOKEN/telemetry` de ese dispositivo)
3. Si el POST de laptop funciona y el ESP32 no:
   - TB_HOST no puede ser localhost (tiene que ser la IP LAN)
   - Wi‑Fi 2.4 GHz, no 5 GHz
   - monitor serie 115200: ¿`WiFi OK`? ¿`POST → 200` o `401`?
   - cableado GPIO 4 + pull-up (4.7 kΩ en DS18B20)
4. Entrega: causa más probable, evidencia (una línea de log o HTTP
   status) y el siguiente comando concreto que debo correr yo.

No ejecutes `docker compose down -v`. No cambies la imagen de
ThingsBoard.

---
