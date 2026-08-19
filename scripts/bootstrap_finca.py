#!/usr/bin/env python3
"""Crea la finca demo, dos sensores de temperatura y guarda sus tokens.

Idempotente: si el customer o los dispositivos ya existen, los reutiliza.
Escribe secrets/devices.json (gitignorado) para el sensor virtual y el ESP32.
"""
from __future__ import annotations

import json
import sys

from tb_client import ROOT, ThingsBoard, load_env, post_attributes, tb_url

CUSTOMER_TITLE = "Finca Demo"
DEVICES = [
    {
        "name": "establo-norte-temp-01",
        "type": "sensor_temperatura",
        "label": "Temperatura establo norte",
        "attributes": {
            "finca": "Finca Demo",
            "lote": "establo-norte",
            "sensor": "DHT22",
            "firmware": "virtual/1.0",
        },
    },
    {
        "name": "lecheria-sombra-temp-01",
        "type": "sensor_temperatura",
        "label": "Temperatura lechería",
        "attributes": {
            "finca": "Finca Demo",
            "lote": "lecheria",
            "sensor": "DS18B20",
            "firmware": "virtual/1.0",
        },
    },
]


def main() -> int:
    env = load_env()
    base = tb_url(env)
    tb = ThingsBoard(base)
    print(f"Conectando a {base} como {env['TB_TENANT_EMAIL']} ...")
    try:
        tb.login(env["TB_TENANT_EMAIL"], env["TB_TENANT_PASSWORD"])
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: no pude entrar. ¿Está arriba ThingsBoard? {exc}", file=sys.stderr)
        print("Prueba: bash scripts/install.sh", file=sys.stderr)
        return 1

    customer = tb.ensure_customer(CUSTOMER_TITLE)
    customer_id = customer["id"]["id"]
    print(f"Customer: {CUSTOMER_TITLE} ({customer_id})")

    secrets_dir = ROOT / "secrets"
    secrets_dir.mkdir(exist_ok=True)
    out_devices = []

    for spec in DEVICES:
        device = tb.ensure_device(
            spec["name"], spec["type"], spec["label"], customer_id=customer_id
        )
        device_id = device["id"]["id"]
        token = tb.device_token(device_id)
        try:
            post_attributes(base, token, spec["attributes"])
        except Exception as exc:  # noqa: BLE001
            print(f"AVISO: no pude publicar atributos de {spec['name']}: {exc}", file=sys.stderr)
        record = {
            "name": spec["name"],
            "label": spec["label"],
            "type": spec["type"],
            "device_id": device_id,
            "access_token": token,
            "http_telemetry": f"{base}/api/v1/{token}/telemetry",
            "mqtt": {
                "host": "127.0.0.1",
                "port": int(env.get("TB_MQTT_PORT", "1883")),
                "username": token,
                "password": "",
                "topic": "v1/devices/me/telemetry",
            },
        }
        out_devices.append(record)
        print(f"Dispositivo {spec['name']}")
        print(f"  token: {token}")
        print(f"  HTTP:  {record['http_telemetry']}")

    payload = {
        "tb_url": base,
        "customer": CUSTOMER_TITLE,
        "devices": out_devices,
    }
    out_path = secrets_dir / "devices.json"
    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"\nGuardado en {out_path.relative_to(ROOT)}")
    print("Siguiente paso: python3 scripts/send_demo_telemetry.py --once")
    print("Luego abre Entities → Devices en la UI y mira Latest telemetry.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
