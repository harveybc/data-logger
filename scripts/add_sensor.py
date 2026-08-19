#!/usr/bin/env python3
"""Registra un sensor nuevo en la finca y imprime el token para el ESP32.

  python3 scripts/add_sensor.py \
      --name pozo-temp-01 \
      --lote pozo \
      --sensor DS18B20 \
      --customer "Finca Demo"
"""
from __future__ import annotations

import argparse
import json
import sys

from tb_client import ROOT, ThingsBoard, load_env, post_attributes, tb_url


def main() -> int:
    parser = argparse.ArgumentParser(description="Crea un dispositivo de temperatura en ThingsBoard.")
    parser.add_argument("--name", required=True, help="Nombre único, ej. establo-sur-temp-01")
    parser.add_argument("--lote", default="sin-lote")
    parser.add_argument("--sensor", default="DHT22", choices=("DHT22", "DHT11", "DS18B20", "otro"))
    parser.add_argument("--customer", default="Finca Demo")
    parser.add_argument("--label", default="")
    args = parser.parse_args()

    env = load_env()
    base = tb_url(env)
    tb = ThingsBoard(base)
    tb.login(env["TB_TENANT_EMAIL"], env["TB_TENANT_PASSWORD"])

    customer = tb.ensure_customer(args.customer)
    label = args.label or f"Temperatura {args.lote}"
    device = tb.ensure_device(args.name, "sensor_temperatura", label, customer["id"]["id"])
    token = tb.device_token(device["id"]["id"])
    post_attributes(
        base,
        token,
        {
            "finca": args.customer,
            "lote": args.lote,
            "sensor": args.sensor,
            "firmware": "pending",
        },
    )

    record = {
        "name": args.name,
        "label": label,
        "customer": args.customer,
        "device_id": device["id"]["id"],
        "access_token": token,
        "http_telemetry": f"{base}/api/v1/{token}/telemetry",
        "mqtt": {
            "host": "IP-DEL-SERVIDOR",
            "port": int(env.get("TB_MQTT_PORT", "1883")),
            "username": token,
            "password": "",
            "topic": "v1/devices/me/telemetry",
        },
    }
    secrets = ROOT / "secrets"
    secrets.mkdir(exist_ok=True)
    out = secrets / f"{args.name}.json"
    out.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")

    print(f"Dispositivo: {args.name}")
    print(f"Token:       {token}")
    print(f"HTTP POST:   {record['http_telemetry']}")
    print(f"Guardado:    {out.relative_to(ROOT)}")
    print()
    print("En firmware/esp32_*/secrets.h:")
    print(f'  #define TB_TOKEN  "{token}"')
    print('  #define TB_HOST   "IP-DEL-SERVIDOR"   // la IP LAN de este computador')
    print("  #define TB_PORT   8080")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
