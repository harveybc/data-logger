# data-logger

**Estado: puente a ThingsBoard CE, listo para el primer ESP32.**

Este repositorio **no es un servidor IoT**. Es el kit que deja armada
[ThingsBoard Community Edition](https://thingsboard.io/) 4.3.1.3 — compose,
tokens, firmware de temperatura y prompts para un agente — para que
personal no técnico vea sensores en el celular sin programar un backend.

El Flask + AdminLTE que vivía aquí (AAA casero, plugins, GUI autogenerada)
está retirado. La historia de git lo conserva; el árbol actual es solo el
puente. Detalle en [`docs/LEGACY.md`](docs/LEGACY.md).

No predice precios. No lee el correo (eso será Hermes, después, escribiendo
al mismo ThingsBoard).

## Úsalo con un agente (como en DOIN)

Si tienes Claude, Cursor, Codex, Copilot o Grok con acceso a la
terminal, no hace falta que recuerdes Docker. Abre este repositorio en
el agente y pega **uno** de estos bloques.

### 1. Levantar la plataforma

> Lee `AGENTS.md` de este repositorio y sigue el **Agent quickstart**
> de punta a punta: comprueba Docker, no toques contenedores ajenos,
> corre `bash scripts/install.sh`, luego `python3 scripts/bootstrap_finca.py`
> y `python3 scripts/send_demo_telemetry.py --once`. Dime la URL para
> abrir ThingsBoard, el usuario y la clave, dónde quedaron los tokens,
> y una cosa que deba probar primero en la UI.

Más variantes (añadir un ESP32, dar de alta otro customer, diagnosticar)
están en [`prompts/`](prompts/) listas para copiar y pegar.

`AGENTS.md` sigue la convención [agents.md](https://agents.md): la
mayoría de agentes lo leen solos.

## Qué vas a ver

1. Una página web en `http://IP-DEL-SERVIDOR:8080`.
2. Dos sensores de mentira (*establo norte* y *lechería*) mandando
   temperatura desde este mismo computador.
3. Tu ESP32, cuando lo flashees, apareciendo al lado.

## Requisitos

- Un computador o VPS con **Docker** y **Docker Compose v2**.
- 2 CPU / 4 GB RAM de holgura (PoC). En producción chica, 8 GB.
- Python 3 (ya viene en Linux/macOS) — los scripts no instalan paquetes.
- Para el hardware: un ESP32, un DHT22 o un DS18B20, y Wi‑Fi 2.4 GHz.

## A mano, sin agente

```bash
cd data-logger
cp .env.example .env          # cambia puertos solo si 8080/1883 están ocupados
bash scripts/install.sh       # primera vez: varios minutos
python3 scripts/bootstrap_finca.py
python3 scripts/send_demo_telemetry.py --once
```

Abre **http://127.0.0.1:8080**

| Quién | Correo | Clave |
|---|---|---|
| Administrador | tenant@thingsboard.org | tenant |
| Super-admin (casi no se usa) | sysadmin@thingsboard.org | sysadmin |

*Entities → Devices → `establo-norte-temp-01` → Latest telemetry*.
Ahí tiene que estar `temperature`.

Cambia esas claves antes de abrir el 8080 a una red. HTTPS (para
usarlo fuera de la LAN) es un Caddy o nginx delante, no un cambio de
ThingsBoard.

## Desempolvar el ESP32

Guía corta: [`firmware/README.md`](firmware/README.md).

```bash
python3 scripts/add_sensor.py --name establo-norte-temp-02 --lote establo-norte --sensor DS18B20
cp firmware/secrets.h.example firmware/esp32_ds18b20_http/secrets.h
# edita Wi-Fi, TB_HOST = IP LAN de este PC, TB_TOKEN = el que imprimió add_sensor
```

HTTP primero (`esp32_dht22_http` o `esp32_ds18b20_http`). MQTT es
opcional. `TB_HOST` **nunca** es `localhost`: el ESP32 no es este
computador.

## Cómo se organiza el acceso

```
quien opera la plataforma  →  Tenant en ThingsBoard
cada cliente / sitio       →  Customer
cada usuario final         →  usuario de ese customer (solo ve lo suyo)
cada sensor                →  Device
```

Detalle en [`docs/TENANTS.md`](docs/TENANTS.md). ThingsBoard CE no cobra
por sensor.

## Qué hay en el repo

| Carpeta | Para qué |
|---|---|
| `docker-compose.yml` | ThingsBoard + su base. La base no se publica en el puerto 5432 del host |
| `scripts/` | Instalar, crear el customer demo, registrar sensor, mandar datos de prueba |
| `firmware/` | Sketches: pluviómetro, DHT/DS18B20, nivel de tanque, hop ESP-NOW |
| `docs/` | Arquitectura, ingestión, recintos, hop, pluviómetro, diseño |
| `prompts/` | Textos listos para un agente |
| `hermes/` | Solo el contrato: más adelante el correo entra por el mismo HTTP |
| `secrets/` | Tokens (no se suben a git) |

## Parar y borrar

```bash
docker compose stop          # apaga, conserva dispositivos y series
docker compose down          # apaga, conserva el volumen
docker compose down -v       # BORRA todos los datos. Pídelo dos veces.
```

## Documentación oficial

- Instalar con Docker: <https://thingsboard.io/docs/user-guide/install/docker/>
- HTTP de dispositivos: <https://thingsboard.io/docs/reference/http-api/>
- MQTT de dispositivos: <https://thingsboard.io/docs/reference/mqtt-api/>
