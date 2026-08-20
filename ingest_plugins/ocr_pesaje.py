"""OCR de la planilla semanal (lunes/martes) → filas fecha,placa,litros_am,litros_pm.

Requiere tesseract en el PATH (`sudo apt install tesseract-ocr`).
El operario escribe a mano: no adivinamos vacas que no se lean.
"""
from __future__ import annotations

import csv
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any

plugin_params = {}


def ocr_image(path: str | Path) -> str:
    path = Path(path)
    try:
        out = subprocess.check_output(
            ["tesseract", str(path), "stdout", "-l", "spa+eng"],
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("Instala tesseract-ocr (apt) para el pesaje por foto.") from exc
    return out


def parse_text(text: str, fecha_default: str | None = None) -> list[dict[str, Any]]:
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        nums = re.findall(r"\d+(?:[.,]\d+)?", line)
        if len(nums) < 2:
            continue
        fecha = fecha_default
        m = re.search(r"(\d{4}-\d{2}-\d{2}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4})", line)
        if m:
            fecha = m.group(1)
            if "/" in fecha or fecha.count("-") == 2 and len(fecha) < 10:
                parts = re.split(r"[/-]", fecha)
                if len(parts) == 3:
                    d, mo, y = parts[0], parts[1], parts[2]
                    if int(y) < 100:
                        y = str(2000 + int(y))
                    if int(d) > 12:
                        fecha = f"{y}-{int(mo):02d}-{int(d):02d}"
                    else:
                        fecha = f"{y}-{int(mo):02d}-{int(d):02d}"
        placa = re.sub(r"\d+(?:[.,]\d+)?", " ", line)
        placa = re.sub(r"\s+", " ", placa).strip(" -")
        if not placa or not fecha:
            continue
        am = float(nums[-2].replace(",", "."))
        pm = float(nums[-1].replace(",", "."))
        rows.append({"fecha": fecha, "placa": placa, "litros_am": am, "litros_pm": pm})
    return rows


def parse(path: str | Path, fecha_default: str | None = None) -> list[dict[str, Any]]:
    return parse_text(ocr_image(path), fecha_default=fecha_default)


def write_csv(rows: list[dict[str, Any]], dest: str | Path) -> Path:
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["fecha", "placa", "litros_am", "litros_pm"])
        w.writeheader()
        w.writerows(rows)
    return dest
