# data-logger

Kit para ver sensores en el celular o el computador **sin programar un
servidor**. Por debajo corre
[ThingsBoard Community Edition](https://thingsboard.io/) 4.3.1.3: la
plataforma guarda series, usuarios y alarmas. Este repositorio solo la
deja armada y trae el firmware para ESP32.

Sirve para telemetría chica que se puede repetir en varios sitios
(lluvia, temperatura, nivel de tanque, y más adelante otros orígenes).
Un sitio no ve los dispositivos de otro.

Código: <https://github.com/harveybc/data-logger>

| Guía | Enlace |
|---|---|
| Pedido de hardware (4 juegos) | [docs/BOM.md](https://github.com/harveybc/data-logger/blob/master/docs/BOM.md) |
| Plan de la aplicación | [docs/PLAN.md](https://github.com/harveybc/data-logger/blob/master/docs/PLAN.md) |
| Cómo crear los agentes | [docs/AGENTES.md](https://github.com/harveybc/data-logger/blob/master/docs/AGENTES.md) |
| Interfaz (Producción / Clima / Calidad) | abajo, `python3 -m app.main` |
| Pluviómetro | [docs/PLUVIOMETRO.md](https://github.com/harveybc/data-logger/blob/master/docs/PLUVIOMETRO.md) |
| Firmware | [firmware/README.md](https://github.com/harveybc/data-logger/blob/master/firmware/README.md) |

## Úsalo con un agente

Si tienes un asistente de código con terminal (Claude, Cursor, Codex,
Copilot, Grok, …), abre **este** repositorio y pega:

> Lee `AGENTS.md` y sigue el **Agent quickstart**: comprueba Docker,
> no detengas contenedores ajenos, corre `bash scripts/install.sh`,
> luego `python3 scripts/bootstrap_finca.py` y
> `python3 scripts/send_demo_telemetry.py --once`. Dime la URL de
> ThingsBoard, usuario y clave, dónde quedaron los tokens, y una cosa
> que deba probar primero en la UI.

Más tareas (añadir un ESP32, otro sitio, diagnosticar) están en
[`prompts/`](https://github.com/harveybc/data-logger/tree/master/prompts).

## Qué vas a ver

1. Una página en `http://IP-DEL-SERVIDOR:8080`.
2. Dos sensores de prueba mandando temperatura desde el computador.
3. Tus ESP32, cuando los flashees, en la misma lista.

## Interfaz web (plugin)

Misma idea de siempre: un JSON global, cada plugin con su bloque, un
**pipeline** que los carga. Hoy el pipeline arranca el plugin
`adminlte` (menú: Producción, Clima, Calidad).

```bash
pip install -r requirements.txt
PYTHONPATH=. python3 -m app.main --load_config examples/config/leche_default.json
```

Abre **http://127.0.0.1:5000**. Menú: Producción, Clima, Calidad, Pastoreo.
Roles de prueba: `?rol=admin`, `veterinario` (sin accounting ni usuarios),
`operario` (solo lectura, sin calidad). Varios sitios por usuario, sin GPS.
Producción y calidad leen una SQLite local alimentada por documentos:

```bash
PYTHONPATH=. python3 -m app.ingest --email examples/fixtures/recoleccion_email.txt
PYTHONPATH=. python3 -m app.ingest --pesaje examples/fixtures/pesaje_semanal.csv
PYTHONPATH=. python3 -m app.ingest --planilla /ruta/liquidacion.pdf
```

No hay ETL de sensores. Detalle: [docs/DATOS.md](https://github.com/harveybc/data-logger/blob/master/docs/DATOS.md).

El software es libre; hospedar y soportar sitios puede ser un servicio
de pago. Ver [docs/SERVICIO.md](https://github.com/harveybc/data-logger/blob/master/docs/SERVICIO.md).

## Requisitos

- Computador o VPS con **Docker** y **Docker Compose v2**.
- 2 CPU / 4 GB de holgura para probar. En producción chica, 8 GB.
- Python 3 (ya viene en Linux y macOS). Los scripts no instalan paquetes.
- Hardware: ESP32 y Wi‑Fi **2.4 GHz**. El primer instrumento de campo
  es un pluviómetro de cubeta (ver compras).

## A mano, sin agente

```bash
git clone https://github.com/harveybc/data-logger.git
cd data-logger
cp .env.example .env          # cambia puertos solo si 8080 o 1883 están ocupados
bash scripts/install.sh       # primera vez: varios minutos
python3 scripts/bootstrap_finca.py
python3 scripts/send_demo_telemetry.py --once
```

Abre **http://127.0.0.1:8080**

| Quién | Correo | Clave |
|---|---|---|
| Administrador | tenant@thingsboard.org | tenant |
| Super-admin (casi no se usa) | sysadmin@thingsboard.org | sysadmin |

*Entities → Devices →* elige un dispositivo → *Latest telemetry*.

Cambia esas claves antes de abrir el 8080 a una red. HTTPS (acceso
fuera de la LAN) es un Caddy o nginx delante, no un cambio de
ThingsBoard.

## Un ESP32 de verdad

```bash
python3 scripts/add_sensor.py --name lluvia-01 --lote meteo --sensor pluviometro
cp firmware/secrets.h.example firmware/esp32_tipping_bucket_http/secrets.h
# Wi-Fi, TB_HOST = IP LAN de este PC, TB_TOKEN = el que imprimió add_sensor
```

Guía: [firmware/README.md](https://github.com/harveybc/data-logger/blob/master/firmware/README.md).
`TB_HOST` **nunca** es `localhost`: el ESP32 no es este computador.

## Varios sitios

```
quien opera la plataforma  →  Tenant
cada cliente / sitio       →  Customer
cada usuario final         →  solo ve los dispositivos de su sitio
cada sensor                →  Device
```

Detalle: [docs/TENANTS.md](https://github.com/harveybc/data-logger/blob/master/docs/TENANTS.md).

## Carpetas

| Carpeta | Para qué |
|---|---|
| `docker-compose.yml` | ThingsBoard y su base (la base no se publica en el 5432 del host) |
| `app/`, `pipeline_plugins/`, `web_plugins/` | Entrada, pipeline y UI AdminLTE |
| `examples/config/` | JSON global + bloques por plugin |
| `scripts/` | Instalar, registrar dispositivos, mandar datos de prueba |
| `firmware/` | Sketches Arduino (cubeta, DHT/DS18B20, tanque, hop) |
| `docs/` | Arquitectura, compras, recintos, ingestión |
| `prompts/` | Textos para pegarle a un agente |
| `secrets/` | Tokens (no se suben a git) |

## Parar

```bash
docker compose stop          # apaga, conserva datos
docker compose down          # apaga, conserva el volumen
docker compose down -v       # BORRA todos los datos
```

## ThingsBoard (oficial)

- [Instalar con Docker](https://thingsboard.io/docs/user-guide/install/docker/)
- [HTTP de dispositivos](https://thingsboard.io/docs/reference/http-api/)
- [MQTT de dispositivos](https://thingsboard.io/docs/reference/mqtt-api/)
