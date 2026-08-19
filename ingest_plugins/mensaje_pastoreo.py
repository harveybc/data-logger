"""Parsea mensajes de cambio de potrero o fertilización (grupo / Telegram).

Ejemplos:
  17/08 tarde salieron del 3 y entraron al 5
  hoy en la mañana salieron de El Alto y entraron a La Vega
  17/08 fertilizamos el potrero 2 con urea 8 bultos

Si un nombre no se resuelve, needs_clarification=True (el agente
preguntará en el grupo más adelante).
"""
from __future__ import annotations

import re
from datetime import date
from typing import Any

plugin_params = {}

_MOMENTO = (
    (r"ma[ñn]ana|am\b", "am"),
    (r"tarde|pm\b", "pm"),
)


def _fecha(text: str) -> str:
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", text)
    if m:
        return m.group(0)
    m = re.search(r"(\d{1,2})[/-](\d{1,2})(?:[/-](\d{2,4}))?", text)
    if m:
        d, mo, y = int(m.group(1)), int(m.group(2)), m.group(3)
        year = int(y) if y else date.today().year
        if year < 100:
            year += 2000
        return f"{year:04d}-{mo:02d}-{d:02d}"
    if re.search(r"\bhoy\b", text, re.I):
        return date.today().isoformat()
    return date.today().isoformat()


def _momento(text: str) -> str | None:
    for pat, val in _MOMENTO:
        if re.search(pat, text, re.I):
            return val
    return None


def _token(chunk: str) -> str:
    return re.sub(r"\s+", " ", chunk).strip(" .,:;")


def parse(text: str) -> dict[str, Any]:
    text = text.strip()
    fecha = _fecha(text)
    momento = _momento(text)

    fert = re.search(
        r"fertiliz|abon|bulto",
        text,
        re.I,
    )
    if fert:
        potrero = None
        m = re.search(
            r"potrero\s+(\d+|[A-Za-zÁÉÍÓÚñ][\wÁÉÍÓÚñ ]{1,40})",
            text,
            re.I,
        )
        if m:
            potrero = _token(m.group(1))
        abono = None
        m = re.search(r"con\s+([A-Za-zÁÉÍÓÚñ0-9][\wÁÉÍÓÚñ -]{1,40})", text, re.I)
        if m:
            abono = _token(re.sub(r"\d+\s*bultos?", "", m.group(1), flags=re.I))
        bultos = None
        m = re.search(r"(\d+(?:[.,]\d+)?)\s*bultos?", text, re.I)
        if m:
            bultos = float(m.group(1).replace(",", "."))
        return {
            "kind": "fertilizacion",
            "fecha": fecha,
            "potrero": potrero,
            "abono": abono or None,
            "bultos": bultos,
            "needs_clarification": not potrero,
            "raw": text,
        }

    salida = entrada = None
    m = re.search(
        r"salieron?\s+(?:del?|de)\s+(?:potrero\s+)?(\d+|[A-Za-zÁÉÍÓÚñ][\wÁÉÍÓÚñ ]{0,40}?)"
        r"\s+y\s+entraron?\s+(?:al?|a)\s+(?:potrero\s+)?(\d+|[A-Za-zÁÉÍÓÚñ][\wÁÉÍÓÚñ ]{0,40})",
        text,
        re.I,
    )
    if m:
        salida, entrada = _token(m.group(1)), _token(m.group(2))
    else:
        m = re.search(r"salieron?\s+(?:del?|de)\s+(?:potrero\s+)?(\d+|[A-Za-zÁÉÍÓÚñ][\wÁÉÍÓÚñ ]{1,40})", text, re.I)
        if m:
            salida = _token(m.group(1))
        m = re.search(r"entraron?\s+(?:al?|a)\s+(?:potrero\s+)?(\d+|[A-Za-zÁÉÍÓÚñ][\wÁÉÍÓÚñ ]{1,40})", text, re.I)
        if m:
            entrada = _token(m.group(1))

    unclear = not (salida or entrada)
    return {
        "kind": "movimiento",
        "fecha": fecha,
        "momento": momento,
        "salida": salida,
        "entrada": entrada,
        "needs_clarification": unclear,
        "raw": text,
    }
