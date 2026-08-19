#!/usr/bin/env python3
"""Sensor virtual: manda temperatura (y humedad) a los dispositivos del bootstrap.

Úsalo para probar la plataforma ANTES de encender un ESP32.

  python3 scripts/send_demo_telemetry.py --once
  python3 scripts/send_demo_telemetry.py --interval 10
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time

from tb_client import ROOT, load_env, post_telemetry, tb_url

SECRETS = ROOT / "secrets" / "devices.json"


def load_devices() -> list[dict]:
    if not SECRETS.exists():
        raise FileNotFoundError(
            "No existe secrets/devices.json. Corre primero:\n"
            "  python3 scripts/bootstrap_finca.py"
        )
    data = json.loads(SECRETS.read_text(encoding="utf-8"))
    return data["devices"]


def sample_for(name: str) -> dict:
    # Rangos creíbles de trópico andino / lechería.
    if "lecheria" in name:
        temp = round(random.uniform(8.0, 14.0), 2)
        payload = {"temperature": temp, "rssi": random.randint(-75, -45)}
    else:
        temp = round(random.uniform(16.0, 28.0), 2)
        hum = round(random.uniform(55.0, 90.0), 1)
        payload = {
            "temperature": temp,
            "humidity": hum,
            "rssi": random.randint(-80, -40),
        }
    return payload


def send_round(base: str, devices: list[dict]) -> None:
    for device in devices:
        payload = sample_for(device["name"])
        status = post_telemetry(base, device["access_token"], payload)
        keys = ", ".join(f"{k}={v}" for k, v in payload.items())
        print(f"HTTP {status}  {device['name']}: {keys}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Envía telemetría de prueba a ThingsBoard.")
    parser.add_argument("--once", action="store_true", help="Una sola ronda y sale.")
    parser.add_argument("--interval", type=int, default=15, help="Segundos entre rondas (default 15).")
    parser.add_argument("--rounds", type=int, default=0, help="Número de rondas (0 = infinito).")
    args = parser.parse_args()

    env = load_env()
    base = tb_url(env)
    try:
        devices = load_devices()
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        return 1

    print(f"Enviando a {base} ({len(devices)} dispositivos). Ctrl+C para parar.")
    n = 0
    try:
        while True:
            send_round(base, devices)
            n += 1
            if args.once or (args.rounds and n >= args.rounds):
                break
            time.sleep(max(1, args.interval))
    except KeyboardInterrupt:
        print("\nDetenido.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
