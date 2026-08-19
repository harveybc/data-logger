"""Parsea el PDF/texto de liquidación Colácteos (calidad + litros/día)."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Any

plugin_params = {}


def extract_text(path: str | Path) -> str:
    path = Path(path)
    try:
        out = subprocess.check_output(
            ["pdftotext", "-layout", str(path), "-"],
            stderr=subprocess.DEVNULL,
            text=True,
        )
        if out.strip():
            return out
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass
    try:
        from pypdf import PdfReader  # type: ignore

        reader = PdfReader(str(path))
        return "\n".join((p.extract_text() or "") for p in reader.pages)
    except Exception as exc:
        raise RuntimeError(f"No pude leer PDF {path}: {exc}") from exc


def _floats(line: str) -> list[float]:
    return [float(x.replace(",", "")) for x in re.findall(r"\d+(?:[.,]\d+)?", line)]


def _money(s: str) -> float:
    s = s.strip()
    if re.match(r"^\d{1,3}(,\d{3})+\.\d{2}$", s):
        return float(s.replace(",", ""))
    if re.match(r"^\d{1,3}(\.\d{3})+,\d{2}$", s):
        return float(s.replace(".", "").replace(",", "."))
    return float(s.replace(",", ""))


def _codigo(text: str) -> str | None:
    m = re.search(
        r"C[oó]digo(?:\s+del)?\s+Productor:?\s*(\d{5,})",
        text,
        re.I,
    )
    if m:
        return m.group(1)
    idx = text.lower().find("c\u00f3digo productor")
    if idx < 0:
        idx = text.lower().find("codigo productor")
    if idx >= 0:
        m = re.search(r"\b(\d{5,6})\b", text[idx : idx + 250])
        if m:
            return m.group(1)
    return None


def parse_text(text: str) -> tuple[dict[str, Any], list[dict]]:
    def after(label: str) -> str | None:
        m = re.search(rf"{label}\s+(\S+)", text, re.I)
        return m.group(1).strip() if m else None

    proteina = grasa = solidos = ufc = None
    for line in text.splitlines():
        nums = _floats(line)
        if "Prote" in line and len(nums) >= 1:
            proteina = nums[0]
        elif re.search(r"Grasa", line, re.I) and len(nums) >= 1:
            grasa = nums[0]
        elif re.search(r"S.?lidos Totales", line, re.I) and len(nums) >= 1:
            solidos = nums[0]
        elif "UFC" in line:
            nums = [n for n in nums if n != 1000]
            if nums:
                ufc = nums[0]

    precio = None
    m = re.search(r"PRECIO POR LITRO.*?([\d.,]+)", text, re.I | re.S)
    if m:
        try:
            precio = _money(m.group(1))
        except ValueError:
            precio = None
    m2 = re.search(r"PRECIO FINAL POR LITRO\s+([\d.,]+)", text, re.I)
    precio_final = _money(m2.group(1)) if m2 else precio

    total_litros = None
    m = re.search(r"No\.\s*Total de Litros\s+([\d.,]+)", text, re.I)
    if m:
        total_litros = float(m.group(1).replace(",", ""))

    total_pagar = None
    m = re.search(r"TOTAL A PAGAR[^\d]*([\d.]+,\d{2}|[\d.]+)", text, re.I)
    if m:
        raw = m.group(1)
        if "," in raw:
            total_pagar = float(raw.replace(".", "").replace(",", "."))
        elif raw.count(".") > 1:
            total_pagar = float(raw.replace(".", ""))
        else:
            total_pagar = float(raw)

    row = {
        "periodo_desde": after("Periodo liquidado"),
        "periodo_hasta": after("Hasta el día") or after("Fecha de liquidación"),
        "codigo_productor": _codigo(text),
        "precio_litro": precio,
        "proteina_pct": proteina,
        "grasa_pct": grasa,
        "solidos_pct": solidos,
        "ufc_x1000": ufc,
        "frio_c": None,
        "precio_final_litro": precio_final,
        "total_litros": total_litros,
        "total_pagar": total_pagar,
        "raw": text[:8000],
    }

    litros_dia: list[dict] = []
    # Fila de fechas jul-16 … y la de litros debajo.
    month_map = {
        "ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6,
        "jul": 7, "ago": 8, "sep": 9, "oct": 10, "nov": 11, "dic": 12,
    }
    lines = text.splitlines()
    for i, line in enumerate(lines):
        heads = re.findall(r"(ene|feb|mar|abr|may|jun|jul|ago|sep|oct|nov|dic)-(\d{1,2})", line, re.I)
        if len(heads) >= 8 and i + 1 < len(lines):
            year = 2026
            if row.get("periodo_desde"):
                year = int(str(row["periodo_desde"])[:4])
            vals = _floats(lines[i + 1])
            for (mon, day), val in zip(heads, vals):
                mm = month_map[mon.lower()[:3]]
                litros_dia.append(
                    {"fecha": f"{year}-{mm:02d}-{int(day):02d}", "litros": val}
                )
            break
    return row, litros_dia


def parse(path: str | Path) -> tuple[dict[str, Any], list[dict]]:
    return parse_text(extract_text(path))
