"""CSV semanal: fecha, placa, litros_am, litros_pm."""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Iterator

plugin_params = {}


def parse(path: str | Path) -> Iterator[dict[str, Any]]:
    with Path(path).open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for raw in reader:
            yield {
                "fecha": (raw.get("fecha") or "").strip(),
                "placa": (raw.get("placa") or raw.get("nombre") or "").strip(),
                "litros_am": float(raw.get("litros_am") or 0),
                "litros_pm": float(raw.get("litros_pm") or 0),
            }
