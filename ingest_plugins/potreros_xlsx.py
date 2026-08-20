"""Excel de potreros. Columnas flexibles: sitio, numero/nro/id, nombre, geojson o wkt."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterator

plugin_params = {}


def _cell(row: dict, *names: str) -> str:
    lower = {str(k).strip().lower(): v for k, v in row.items()}
    for n in names:
        v = lower.get(n)
        if v is not None and str(v).strip():
            return str(v).strip()
    return ""


def parse(path: str | Path) -> Iterator[dict[str, Any]]:
    try:
        import openpyxl
    except ImportError as exc:
        raise RuntimeError("pip install openpyxl  para leer .xlsx") from exc
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        return
    headers = [str(h or "").strip() for h in rows[0]]
    for raw in rows[1:]:
        row = dict(zip(headers, raw))
        numero = _cell(row, "numero", "nro", "id", "potrero", "codigo")
        nombre = _cell(row, "nombre", "name", "potrero") or numero
        if not numero:
            continue
        geo = _cell(row, "geojson", "wkt", "poligono", "polygon")
        if geo and not geo.startswith("{"):
            geo = json.dumps({"type": "Polygon", "wkt": geo})
        yield {
            "sitio": _cell(row, "sitio", "finca", "predio") or "Sitio demo",
            "numero": numero,
            "nombre": nombre,
            "geojson": geo or None,
        }
