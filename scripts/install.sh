#!/usr/bin/env bash
# Instala y arranca ThingsBoard CE para el kit de telemetría de finca.
# Idempotente: si ya se inicializó el esquema, solo hace `up -d`.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if ! command -v docker >/dev/null 2>&1; then
  echo "ERROR: Docker no está instalado. Instálalo y vuelve a correr este script." >&2
  exit 1
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "ERROR: Docker Compose v2 no está disponible (comando: docker compose)." >&2
  exit 1
fi

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Creé .env desde .env.example. Edítalo si 8080 o 1883 ya están ocupados."
fi

# shellcheck disable=SC1091
set -a
# Los valores de .env.example / .env son KEY=value simples.
. ./.env
set +a

HTTP_PORT="${TB_HTTP_PORT:-8080}"
MQTT_PORT="${TB_MQTT_PORT:-1883}"

port_busy() {
  local port="$1"
  if command -v ss >/dev/null 2>&1; then
    ss -lntu | awk '{print $5}' | grep -Eq "[:.]${port}$"
  elif command -v netstat >/dev/null 2>&1; then
    netstat -lntu 2>/dev/null | awk '{print $4}' | grep -Eq "[:.]${port}$"
  else
    return 1
  fi
}

echo "Comprobando puertos ${HTTP_PORT} (web) y ${MQTT_PORT} (MQTT)..."
if port_busy "$HTTP_PORT"; then
  echo "AVISO: el puerto ${HTTP_PORT} ya está en uso."
  echo "        Si ThingsBoard no es quien lo usa, cambia TB_HTTP_PORT en .env y reintenta."
fi
if port_busy "$MQTT_PORT"; then
  echo "AVISO: el puerto ${MQTT_PORT} ya está en uso."
  echo "        Si ThingsBoard no es quien lo usa, cambia TB_MQTT_PORT en .env y reintenta."
fi

if [ ! -f .tb-initialized ]; then
  echo "Inicializando esquema de ThingsBoard y datos de demostración (solo la primera vez)..."
  echo "Esto descarga imágenes y puede tardar varios minutos."
  docker compose run --rm -e INSTALL_TB=true -e LOAD_DEMO=true thingsboard-ce
  date -u +"%Y-%m-%dT%H:%M:%SZ" > .tb-initialized
  echo "Esquema listo."
else
  echo "Esquema ya inicializado (.tb-initialized). No vuelvo a correr INSTALL_TB."
fi

echo "Arrancando ThingsBoard..."
docker compose up -d

echo
echo "Esperando a que la UI responda en ${TB_URL:-http://127.0.0.1:${HTTP_PORT}} ..."
python3 scripts/wait_for_tb.py

echo
echo "Listo."
echo "  UI:     ${TB_URL:-http://127.0.0.1:${HTTP_PORT}}"
echo "  Login:  tenant@thingsboard.org  /  tenant"
echo "Siguiente paso:"
echo "  python3 scripts/bootstrap_finca.py"
echo "  python3 scripts/send_demo_telemetry.py --once"
