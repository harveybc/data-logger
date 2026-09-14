# data-logger

Collect sensor (and other) time series into
[ThingsBoard Community Edition](https://thingsboard.io/) and serve them
through **plugins**: JSON config, a pipeline, ESP32 firmware, and optional
web UIs (AdminLTE). Same layout as the rest of this house (`predictor`,
`data-gov`).

Code: <https://github.com/harveybc/data-logger>

| Guide | Link |
|---|---|
| Hardware list | [docs/BOM.md](docs/BOM.md) |
| Architecture | [docs/PLAN.md](docs/PLAN.md) |
| Agent prompts | [docs/AGENTES.md](docs/AGENTES.md) |
| Rain gauge | [docs/PLUVIOMETRO.md](docs/PLUVIOMETRO.md) |
| Firmware | [firmware/README.md](firmware/README.md) |
| Example dashboard plugin | [docs/plugins/agro/README.md](docs/plugins/agro/README.md) |

## Use it with an agent

Open **this** repository in Claude, Cursor, Codex, Copilot, Grok, … and paste:

> Read `AGENTS.md` and follow the **Agent quickstart**: check Docker, do
> not stop containers you did not start, run `bash scripts/install.sh`,
> then `python3 scripts/bootstrap_finca.py` and
> `python3 scripts/send_demo_telemetry.py --once`. Tell me the ThingsBoard
> URL, user and password, where the device tokens are, and one thing I
> should try first in the UI.

More tasks (add an ESP32, another site, diagnose) live in [`prompts/`](prompts/).

## What you get

1. ThingsBoard at `http://IP-OF-THIS-HOST:8080`.
2. Two demo temperature devices from this computer.
3. Real ESP32s, once flashed, in the same device list.

## Requirements

- A machine or VPS with **Docker** and **Docker Compose v2**.
- 2 CPU / 4 GB to try it; ~8 GB for a small production box.
- Python 3 (scripts do not `pip install` for you).
- ESP32 and **2.4 GHz** Wi-Fi.

## Install (no agent)

```bash
git clone https://github.com/harveybc/data-logger.git
cd data-logger
cp .env.example .env          # change ports only if 8080 or 1883 are taken
bash scripts/install.sh       # first time: several minutes
python3 scripts/bootstrap_finca.py
python3 scripts/send_demo_telemetry.py --once
```

Open **http://127.0.0.1:8080**

| Who | Email | Password |
|---|---|---|
| Tenant admin | tenant@thingsboard.org | tenant |
| Super-admin (rarely) | sysadmin@thingsboard.org | sysadmin |

*Entities → Devices →* pick a device → *Latest telemetry*.

Change those passwords before exposing 8080. HTTPS in front is Caddy or
nginx, not a ThingsBoard setting.

## Plugins

A run is a flat JSON file. The pipeline loads the plugins named in it.
Sensor series stay in ThingsBoard. Extra ingest (email, CSV, PDF) is
also plugins; see `ingest_plugins/` and `app.ingest`.

```bash
pip install -r requirements.txt
PYTHONPATH=. python3 -m app.main --load_config examples/config/leche_default.json
```

That example config starts the bundled AdminLTE dashboard on
**http://127.0.0.1:5000**. How that dashboard is built (and how to copy
it) is in [docs/plugins/agro/README.md](docs/plugins/agro/README.md).

Sensor ETL is not in this Flask app. ThingsBoard detail: [docs/DATOS.md](docs/DATOS.md).

The software is MIT; hosting and support can be a paid service.
[docs/SERVICIO.md](docs/SERVICIO.md).

## A real ESP32

```bash
python3 scripts/add_sensor.py --name rain-01 --lote meteo --sensor pluviometro
cp firmware/secrets.h.example firmware/esp32_tipping_bucket_http/secrets.h
# Wi-Fi, TB_HOST = LAN IP of this PC, TB_TOKEN = printed by add_sensor
```

[firmware/README.md](firmware/README.md). `TB_HOST` is **never**
`localhost`: the ESP32 is not this computer.

## Sites (ThingsBoard tenants)

```
platform operator  →  Tenant
each customer      →  Customer
end user           →  only that customer's devices
each sensor        →  Device
```

[docs/TENANTS.md](docs/TENANTS.md).

## Layout

| Path | Role |
|---|---|
| `docker-compose.yml` | ThingsBoard + its DB (Postgres is not published on host 5432) |
| `app/`, `pipeline_plugins/`, `web_plugins/` | Entry, pipeline, web plugins |
| `ingest_plugins/` | Document ingest |
| `examples/config/` | JSON configs |
| `scripts/` | Install, register devices, demo telemetry |
| `firmware/` | Arduino sketches |
| `docs/` | Architecture, BOM, ingest |
| `prompts/` | Paste-blocks for coding agents |
| `secrets/` | Tokens (not in git) |

## Stop

```bash
docker compose stop          # keep data
docker compose down          # keep the volume
docker compose down -v       # WIPES all data
```

## ThingsBoard (upstream)

- [Docker install](https://thingsboard.io/docs/user-guide/install/docker/)
- [HTTP device API](https://thingsboard.io/docs/reference/http-api/)
- [MQTT device API](https://thingsboard.io/docs/reference/mqtt-api/)
