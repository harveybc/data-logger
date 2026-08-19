#!/usr/bin/env bash
# Diagnóstico rápido: Docker, puertos, UI, tokens, una telemetría de prueba.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "=== docker ==="
if command -v docker >/dev/null; then
  docker compose ps || true
else
  echo "Docker no está instalado."
fi

echo
echo "=== puertos ==="
if command -v ss >/dev/null; then
  ss -lntu | grep -E ':8080|:1883|:8883' || echo "(nada escuchando en 8080/1883/8883)"
fi

echo
echo "=== UI ==="
python3 - <<'PY'
import urllib.request, urllib.error
try:
    urllib.request.urlopen("http://127.0.0.1:8080/login", timeout=5)
    print("http://127.0.0.1:8080 responde")
except Exception as exc:
    print("UI no responde:", exc)
PY

echo
echo "=== secrets/devices.json ==="
if [ -f secrets/devices.json ]; then
  python3 - <<'PY'
import json
from pathlib import Path
data = json.loads(Path("secrets/devices.json").read_text())
print("tb_url:", data.get("tb_url"))
for d in data.get("devices", []):
    print(f"  {d['name']}  token={d['access_token'][:8]}…")
PY
else
  echo "No existe. Corre: python3 scripts/bootstrap_finca.py"
fi

echo
echo "=== claves demo ==="
PYTHONPATH=scripts python3 - <<'PY'
from tb_client import ThingsBoard, load_env, tb_url
env = load_env()
email = env.get("TB_TENANT_EMAIL", "")
pwd = env.get("TB_TENANT_PASSWORD", "")
print("tenant:", email)
if email.endswith("@thingsboard.org") or pwd == "tenant":
    print("AVISO: sigues con claves demo. No publiques 8080/1883/8883/7070/CoAP a una red.")
try:
    ThingsBoard(tb_url(env)).login(email, pwd)
    print("login tenant OK")
except Exception as exc:
    print("login tenant FALLÓ:", exc)
PY

echo
echo "=== telemetría de prueba ==="
if [ -f secrets/devices.json ]; then
  python3 scripts/send_demo_telemetry.py --once || true
fi
