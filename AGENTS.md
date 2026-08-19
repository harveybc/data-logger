# AGENTS.md — data-logger

Guidance for AI coding agents working in this repository. See [agents.md](https://agents.md).

## Project overview

`data-logger` is a **bridge / deployment kit** plus a small plugin
pipeline (JSON config, pipeline orchestrator, AdminLTE web plugin).
It wraps ThingsBoard Community Edition 4.3.1.3 (official Docker
image `thingsboard/tb-node:4.3.1.3` + `postgres:18`) with scripts, ESP32
temperature firmware, and copy-paste prompts so a non-technical
operator can stand up device telemetry without writing a backend.

It does **not** parse email or PDFs (that is Hermes, later, injecting
into the same HTTP telemetry API). Login and tenants stay in
ThingsBoard. The new `web_plugins.adminlte` is a *domain* UI
(Producción / Clima / Calidad) on top of TB, not a rewrite of the
retired Flask AAA (`docs/LEGACY.md`). Do not restore that AAA. It is
not a trading system and it does not train models.

Verified against the official install guide:
<https://thingsboard.io/docs/user-guide/install/docker/>

## Agent quickstart (install → ingest → show the user results)

### 0. Safety if this machine already runs other Docker stacks

**Do not stop, restart or recreate any container you did not start.**
**Do not bind host port 5432.** This compose keeps Postgres internal
on purpose.

Before `up`:

```bash
ss -lntu | grep -E ':8080|:1883|:8883|:5432' || true
docker ps --format 'table {{.Names}}\t{{.Ports}}\t{{.Status}}'
```

If 8080 or 1883 are taken, change `TB_HTTP_PORT` / `TB_MQTT_PORT` in
`.env` (copy from `.env.example`). If this machine is busy and the user
did not explicitly ask to start ThingsBoard here, prepare the files and
tell them to run the kit on a spare VPS or laptop instead of forcing it.

Force nothing that needs a GPU. This stack is CPU-only.

### 1. Environment

Docker Engine + Compose v2. Python 3.10+ for the helper scripts (stdlib
only — no `pip install`).

```bash
cd data-logger   # clone or open https://github.com/harveybc/data-logger
cp -n .env.example .env
docker compose version
python3 --version
```

### 2. Smoke test (platform up)

```bash
bash scripts/install.sh
```

`install.sh` is idempotent. First run: `INSTALL_TB=true LOAD_DEMO=true`
(several minutes, pulls images, writes `.tb-initialized`). Later runs:
`docker compose up -d` only.

Proof it worked:

```bash
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8080/login
# expect 200
docker compose ps
```

Login in a browser: `http://127.0.0.1:8080`
tenant `tenant@thingsboard.org` / `tenant`.

### 3. Representative run (create devices + send temperature)

```bash
python3 scripts/bootstrap_finca.py
python3 scripts/send_demo_telemetry.py --once
```

`bootstrap_finca.py` creates customer `Finca Demo` and two devices
(`establo-norte-temp-01`, `lecheria-sombra-temp-01`), prints access
tokens, writes `secrets/devices.json` (gitignored). `--once` POSTs one
JSON telemetry point per device.

Proof: ThingsBoard UI → *Entities → Devices → establo-norte-temp-01 →
Latest telemetry* shows `temperature`, `humidity`, `rssi`. Or:

```bash
python3 - <<'PY'
import json, urllib.request
from pathlib import Path
# Just re-send and print HTTP status; the UI is the real proof.
print(Path('secrets/devices.json').read_text()[:400])
PY
```

To keep a live stream without hardware: `python3 scripts/send_demo_telemetry.py --interval 10`

### 4. ESP32 (only if the user has the board on the desk)

Do **not** flash hardware unless the user asked. Point them at
`firmware/README.md`. HTTP first (`esp32_dht22_http` or
`esp32_ds18b20_http`). `TB_HOST` must be the LAN IP of this machine,
never `localhost`. Token from `bootstrap_finca.py` or:

```bash
python3 scripts/add_sensor.py --name pozo-temp-01 --lote pozo --sensor DS18B20
```

### 5. Analytics / Metabase / OLAP

**There is none in this repo, and none should be added here.**
ThingsBoard *is* the dashboard and the time-series store. Do not stand
up a second analytics stack unless the user asked for it.

### 6. Final message to give the user

> La plataforma está en **http://localhost:8080** (o el `TB_HTTP_PORT`
> que hayas puesto). Entra con `tenant@thingsboard.org` / `tenant`.
> Los sensores demo están en *Entities → Devices*; abre
> `establo-norte-temp-01` y mira *Latest telemetry*.
>
> El archivo con los tokens es `secrets/devices.json` — no lo subas a
> git. Para el ESP32: copia `firmware/secrets.h.example` a
> `firmware/esp32_dht22_http/secrets.h` (o `esp32_ds18b20_http` si es
> DS18B20), pon la IP LAN de este computador en `TB_HOST` y el token
> en `TB_TOKEN`. Guía de pines en `firmware/README.md`.
>
> Primera cosa que probar: deja corriendo
> `python3 scripts/send_demo_telemetry.py --interval 10` y en la UI
> crea un dashboard vacío, arrastra un widget *Timeseries Line Chart*,
> dispositivo `establo-norte-temp-01`, clave `temperature`.

## Layout

| Path | Purpose |
|---|---|
| `docker-compose.yml` | Official TB CE + Postgres; Postgres not published on the host |
| `scripts/install.sh` | First-time schema + `up -d` |
| `scripts/bootstrap_finca.py` | Demo customer + two temperature devices + tokens |
| `scripts/add_sensor.py` | Register one more device, print token for the ESP32 |
| `scripts/send_demo_telemetry.py` | Laptop virtual sensor (no hardware) |
| `scripts/diagnose.sh` | Ports, UI, tokens, one test POST |
| `scripts/tb_client.py` | Tiny REST helper (stdlib) |
| `app/`, `pipeline_plugins/`, `web_plugins/` | Config merge, pipeline, AdminLTE UI |
| `examples/config/` | JSON globals + per-plugin blocks |
| `firmware/` | Arduino: pluviometer, DHT/DS18B20, tank level, ESP-NOW hop/gateway |
| `docs/` | Architecture, ingest, enclosure, hop, pluviometer, design — Spanish |
| `hermes/` | Contract only: later email/PDF injects the same HTTP API |
| `prompts/` | Copy-paste prompts for users to give their coding agent |
| `secrets/` | Generated tokens; gitignored JSON |

## Conventions

- Long-lived state is ThingsBoard + the Docker volume
  `data-logger-tb-postgres-data`. Deleting that volume wipes devices and
  telemetry. Say so before `docker compose down -v`.
- Tokens live in `secrets/`. Never commit them. Never put real Wi-Fi
  passwords in tracked files (`firmware/**/secrets.h` is gitignored).
- Device JSON keys are English (`temperature`, `humidity`, `rssi`) so
  they match ThingsBoard widget defaults and every ESP32 example online.
  UI labels can be Spanish.
- Prefer HTTP telemetry for the first ESP32. MQTT is optional.
- Adding a sensor is data, not code: register device → copy token →
  flash. Do not add Flask routes.

## Do not touch

- Running GPU jobs, existing Docker Postgres/Metabase, or any compose
  project that is not this one.
- `docker compose down -v` on a farm that already has real data.
- Implementing Hermes, a custom AAA, or restoring the retired Flask app.
- Changing the ThingsBoard image tag without an explicit upgrade
  request. Official upgrades are sequential between minor versions.
- Opening 8080 to the internet with the default `tenant`/`sysadmin`
  passwords.

## Build, test and lint

There is no Python package, no pytest suite, no linter, no CI. Scripts
are stdlib. Firmware is compiled on the user's Arduino IDE, not here.

Sanity without Docker (always safe):

```bash
python3 -m py_compile scripts/*.py
```
