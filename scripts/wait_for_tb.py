#!/usr/bin/env python3
"""Espera a que la UI de ThingsBoard responda."""
from __future__ import annotations

import sys
import time
import urllib.error
import urllib.request

from tb_client import load_env, tb_url

TIMEOUT_S = 180
INTERVAL_S = 3


def main() -> int:
    base = tb_url(load_env())
    deadline = time.time() + TIMEOUT_S
    last_err = "sin intentar"
    while time.time() < deadline:
        try:
            req = urllib.request.Request(f"{base}/login", method="GET")
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status in (200, 301, 302):
                    print(f"ThingsBoard responde en {base} (HTTP {resp.status}).")
                    return 0
                last_err = f"HTTP {resp.status}"
        except urllib.error.HTTPError as exc:
            # /login puede devolver 200 HTML; cualquier respuesta HTTP cuenta.
            print(f"ThingsBoard responde en {base} (HTTP {exc.code}).")
            return 0
        except Exception as exc:  # noqa: BLE001 — esperamos conexión rechazada al arrancar
            last_err = str(exc)
        time.sleep(INTERVAL_S)
    print(f"ERROR: ThingsBoard no respondió en {TIMEOUT_S}s ({last_err}).", file=sys.stderr)
    print("Revisa: docker compose logs -f thingsboard-ce", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
