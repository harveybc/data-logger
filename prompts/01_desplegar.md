# Prompt — desplegar la plataforma

Copia todo el recuadro y pégalo en Claude, Cursor, Codex, Copilot o Grok
(el agente necesita acceso a la terminal de **este** computador o del
servidor del sitio).

---

Lee `AGENTS.md` de este repositorio y sigue el **Agent quickstart** de
punta a punta:

1. Comprueba que Docker y `docker compose` existen.
2. No detengas contenedores que no hayas arrancado tú. No publiques el
   puerto 5432. Si 8080 o 1883 están ocupados, cambia `TB_HTTP_PORT` /
   `TB_MQTT_PORT` en `.env`.
3. Corre `bash scripts/install.sh` y espera a que la UI responda.
4. Corre `python3 scripts/bootstrap_finca.py`.
5. Corre `python3 scripts/send_demo_telemetry.py --once`.
6. Dime la URL exacta para abrir ThingsBoard, el usuario y la clave del
   tenant, la ruta de `secrets/devices.json`, y una cosa que deba
   probar primero en la UI (Latest telemetry del sensor
   `establo-norte-temp-01`).

Si algo falla, no improvises otro backend: pega los logs de
`docker compose logs --tail 80 thingsboard-ce` y sigue
`scripts/diagnose.sh`.

---
