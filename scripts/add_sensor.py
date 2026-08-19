#!/usr/bin/env python3
"""Registra un dispositivo en ThingsBoard e imprime el token.

  python3 scripts/add_sensor.py --name pluviometro-01 --lote meteo --sensor pluviometro
  python3 scripts/add_sensor.py --name sombra-01 --sensor DHT22 --hop espnow --source esp32

ensure_device no cambia type/label de un device que ya existe: usa otro --name.
"""
from __future__ import annotations

import argparse
import json
import sys

from tb_client import ROOT, ThingsBoard, load_env, post_attributes, tb_url

TYPE_BY_SENSOR = {
    "pluviometro": "sensor_clima",
    "tank_level": "sensor_nivel",
    "gateway": "gateway",
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Crea un dispositivo en ThingsBoard (type solo aplica al crear)."
    )
    parser.add_argument("--name", required=True)
    parser.add_argument("--lote", default="sin-lote")
    parser.add_argument(
        "--sensor",
        default="DHT22",
        choices=("DHT22", "DHT11", "DS18B20", "pluviometro", "tank_level", "gateway", "otro"),
    )
    parser.add_argument("--source", default="esp32", help="Attribute source (esp32|hermes|script|otro)")
    parser.add_argument("--hop", default="wifi", help="Attribute hop (wifi|espnow|wired|none)")
    parser.add_argument(
        "--type",
        default="",
        help="ThingsBoard device type al CREAR. Si el nombre ya existe, se ignora.",
    )
    parser.add_argument("--customer", default="Finca Demo")
    parser.add_argument("--label", default="")
    parser.add_argument("--create-customer-user", metavar="EMAIL", default="")
    parser.add_argument("--customer-user-password", default="cambiar-ahora")
    args = parser.parse_args()

    env = load_env()
    base = tb_url(env)
    tb = ThingsBoard(base)
    tb.login(env["TB_TENANT_EMAIL"], env["TB_TENANT_PASSWORD"])

    customer = tb.ensure_customer(args.customer)
    if args.create_customer_user:
        tb.create_customer_user(
            customer["id"]["id"],
            args.create_customer_user,
            args.customer_user_password,
        )
        print(f"Customer user: {args.create_customer_user}")

    device_type = args.type or TYPE_BY_SENSOR.get(args.sensor, "sensor_temperatura")
    label = args.label or f"{args.sensor} {args.lote}"
    existing = tb.find_device_by_name(args.name)
    if existing:
        print(
            f"AVISO: {args.name} ya existe; type/label no se actualizan "
            f"(sigue {existing.get('type')})."
        )
    device = tb.ensure_device(args.name, device_type, label, customer["id"]["id"])
    token = tb.device_token(device["id"]["id"])
    post_attributes(
        base,
        token,
        {
            "site": args.customer,
            "lote": args.lote,
            "sensor": args.sensor,
            "source": args.source,
            "hop": args.hop,
            "firmware": "pending",
        },
    )

    record = {
        "name": args.name,
        "label": label,
        "customer": args.customer,
        "type": device_type,
        "source": args.source,
        "hop": args.hop,
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
    print(f"source/hop:  {args.source}/{args.hop}")
    print(f"Guardado:    {out.relative_to(ROOT)}")
    print()
    print("En firmware/<sketch>/secrets.h:")
    print(f'  #define TB_TOKEN  "{token}"')
    print('  #define TB_HOST   "IP-DEL-SERVIDOR"')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
