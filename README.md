# data-logger

Open-source stack to **log sensors and documents into a private ThingsBoard**, then expose them through **plugins** (ingest + optional AdminLTE dashboards).

| Piece | Role |
|---|---|
| ThingsBoard CE 4.3.1.3 | Time series, tenants, devices, alarms |
| ESP32 firmware | HTTP/MQTT tipping-bucket and temp demos |
| Plugin pipeline | Flat JSON config → setuptools entry points (same idea as `predictor`) |
| Ingest plugins | Email, CSV, PDF → local SQLite |
| Web plugins | Domain dashboards on top of TB + SQLite |

Repo: <https://github.com/harveybc/data-logger>

## Docs map

| Doc | Content |
|---|---|
| [docs/PLAN.md](docs/PLAN.md) | Architecture |
| [docs/BOM.md](docs/BOM.md) | Hardware |
| [docs/DATOS.md](docs/DATOS.md) | What lives in ThingsBoard vs SQLite |
| [docs/TENANTS.md](docs/TENANTS.md) | Tenant / customer / device model |
| [docs/PLUVIOMETRO.md](docs/PLUVIOMETRO.md) | Rain gauge |
| [firmware/README.md](firmware/README.md) | Flashing ESP32 |
| [docs/plugins/agro/README.md](docs/plugins/agro/README.md) | Example dashboard + email ingest |
| [docs/AGENTES.md](docs/AGENTES.md) | Who does what (ops) |
| [prompts/](prompts/) | Paste-blocks for coding agents |

## Quick start

**Need:** Docker Compose v2, ~2 CPU / 4 GB RAM (8 GB if you leave it up), Python 3, optional ESP32 on **2.4 GHz** Wi-Fi.

```bash
git clone https://github.com/harveybc/data-logger.git
cd data-logger
cp .env.example .env                 # only touch ports if 8080/1883 clash
bash scripts/install.sh              # first pull can take several minutes
python3 scripts/bootstrap_finca.py   # registers a demo site + devices
python3 scripts/send_demo_telemetry.py --once
```

Open **http://127.0.0.1:8080** → *Entities → Devices → Latest telemetry*.

| Role | Email | Password (change before exposing 8080) |
|---|---|---|
| Tenant admin | `tenant@thingsboard.org` | `tenant` |
| Sysadmin | `sysadmin@thingsboard.org` | `sysadmin` |

Put HTTPS in front with Caddy/nginx if the port leaves the LAN.

### Paste this into a coding agent

> Read `AGENTS.md` and run the **Agent quickstart**. Do not stop Docker
> containers you did not start. Run `bash scripts/install.sh`, then
> `python3 scripts/bootstrap_finca.py` and
> `python3 scripts/send_demo_telemetry.py --once`. Report the ThingsBoard
> URL, login, where device tokens were written, and one UI check to try
> first. If the task is the agro dashboard/email ingest, also read
> `docs/plugins/agro/README.md`.

## How a run works

1. A flat JSON under `examples/config/` names the plugins.
2. `python3 -m app.main --load_config <json>` starts the pipeline.
3. Sensor series go to **ThingsBoard**. Document ingest (email/CSV/PDF) goes to **SQLite** via `app.ingest`.
4. A web plugin (optional) serves AdminLTE on port 5000.

```bash
pip install -r requirements.txt
PYTHONPATH=. python3 -m app.main --load_config examples/config/leche_default.json
# dashboard → http://127.0.0.1:5000
```

`leche_default.json` is the shipped example dashboard. How to clone that
pattern for another domain: [docs/plugins/agro/README.md](docs/plugins/agro/README.md).

## Add a real ESP32

```bash
python3 scripts/add_sensor.py --name rain-01 --lote meteo --sensor pluviometro
cp firmware/secrets.h.example firmware/esp32_tipping_bucket_http/secrets.h
# Set Wi-Fi, TB_HOST = this machine's LAN IP (never localhost), TB_TOKEN from add_sensor
```

Details: [firmware/README.md](firmware/README.md).

## Tenants (multi-site)

```
platform operator  →  Tenant
each customer      →  Customer
end user           →  only that customer's devices
each sensor        →  Device
```

See [docs/TENANTS.md](docs/TENANTS.md).

## Layout

| Path | Role |
|---|---|
| `docker-compose.yml` | ThingsBoard + its Postgres (host 5432 is **not** published) |
| `app/` | CLI entry, IMAP helper, SQLite store |
| `pipeline_plugins/` | Orchestration |
| `web_plugins/` | Dashboards |
| `ingest_plugins/` | Email / CSV / PDF parsers |
| `examples/config/` | JSON configs |
| `scripts/` | Install, bootstrap, demo telemetry, add sensor |
| `firmware/` | Arduino sketches |
| `secrets/` | Device tokens (gitignored) |
| `data/` | Local SQLite (gitignored `*.db`) |

## Stop

```bash
docker compose stop          # keep data
docker compose down          # keep the volume
docker compose down -v       # WIPES all ThingsBoard data
```

## Upstream

- [ThingsBoard Docker install](https://thingsboard.io/docs/user-guide/install/docker/)
- [HTTP device API](https://thingsboard.io/docs/reference/http-api/)
- [MQTT device API](https://thingsboard.io/docs/reference/mqtt-api/)

License: MIT. Hosting/support options: [docs/SERVICIO.md](docs/SERVICIO.md).
