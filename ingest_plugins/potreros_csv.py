"""Carga potreros desde CSV (exportado de Excel).

Columnas: sitio, numero, nombre, geojson
geojson = polígono GeoJSON en una celda, o vacío (se dibuja luego).

Sin GPS de sensores: las coordenadas son del mapa de potreros, no del ESP32.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Iterator

plugin_params = {}


def parse(path: str | Path) -> Iterator[dict[str, Any]]:
    with Path(path).open(encoding="utf-8", newline="") as fh:
        for raw in csv.DictReader(fh):
            geo = (raw.get("geojson") or "").strip()
            if geo:
                json.loads(geo)
            yield {
                "sitio": (raw.get("sitio") or "default").strip(),
                "numero": (raw.get("numero") or "").strip(),
                "nombre": (raw.get("nombre") or raw.get("numero") or "").strip(),
                "geojson": geo or None,
            }
