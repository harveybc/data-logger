"""Parsea el correo de recolección diaria (planta → productor, ~1 día tarde)."""
from __future__ import annotations

import re
from typing import Any

plugin_params = {}


def parse(text: str) -> dict[str, Any]:
    def grab(label: str) -> str | None:
        m = re.search(rf"{label}\s+(\S.*)", text, re.I)
        if not m:
            return None
        return m.group(1).strip()

    def num(label: str) -> float | None:
        raw = grab(label)
        if not raw:
            return None
        return float(raw.replace(",", "").split()[0])

    fecha = grab(r"Fecha")
    return {
        "fecha": fecha,
        "codigo_productor": grab(r"Codigo del productor"),
        "ruta": grab(r"Ruta"),
        "medida_tanque": num(r"Medida del tanque"),
        "litros": num(r"Litros"),
        "conductor": grab(r"Conductor"),
        "compartimiento": grab(r"Compartimiento") or "1",
        "raw": text,
    }
