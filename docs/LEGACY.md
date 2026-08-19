# Qué era este repositorio

Hasta el commit `be895d1` (2024), `data-logger` era un framework Flask
propio: AAA, plugins `core`/`gui`/`store`, AdminLTE, una GUI
autogenerada desde `config_store.json`. En la práctica no era un
producto IoT usable para una finca: no había ingest real de ESP32, el
AAA era casero y la GUI competía con lo que ThingsBoard ya resuelve.

Ese árbol se **retiró** el 2026-08-18. No se reescribe. Git conserva
cada archivo (`git show be895d1:app/app.py`). El árbol actual es solo
el puente: Docker de ThingsBoard CE, scripts, firmware y prompts.

Si un agente encuentra imports de `app.data_logger`, `plugins.core` o
`migrate.sh`, está leyendo historia. No los restaures.
