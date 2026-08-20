#!/usr/bin/env python3
"""Carga correo / PDF / CSV de pesaje a SQLite. No toca ThingsBoard."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.store import Store
from ingest_plugins import (
    email_recoleccion,
    mensaje_pastoreo,
    ocr_pesaje,
    pesaje_semanal,
    planilla_calidad,
    potreros_csv,
    potreros_xlsx,
)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Ingestión de documentos de leche")
    p.add_argument("--db", default="data/app.db")
    p.add_argument("--email", help="Archivo de texto del correo de recolección")
    p.add_argument("--planilla", help="PDF de liquidación / calidad")
    p.add_argument("--pesaje", help="CSV fecha,placa,litros_am,litros_pm")
    p.add_argument("--potreros", help="CSV sitio,numero,nombre,geojson")
    p.add_argument("--potreros-xlsx", help="Excel de potreros")
    p.add_argument("--ocr-pesaje", help="Foto de la planilla AM/PM (tesseract)")
    p.add_argument("--ocr-fecha", help="Fecha ISO si la foto no la trae")
    p.add_argument("--mensaje", help="Texto de cambio de potrero o fertilización")
    p.add_argument("--sitio", default="Sitio demo", help="Sitio para --mensaje")
    p.add_argument("--imap", action="store_true", help="Bajar acopio por IMAP (.env)")
    p.add_argument("--imap-keep", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args(argv)
    if not (
        args.email
        or args.planilla
        or args.pesaje
        or args.potreros
        or args.potreros_xlsx
        or args.ocr_pesaje
        or args.mensaje
        or args.imap
    ):
        p.print_help()
        return 2
    store = Store(args.db)
    if args.email:
        text = Path(args.email).read_text(encoding="utf-8")
        row = email_recoleccion.parse(text)
        if not row.get("fecha") or row.get("litros") is None:
            print("No pude leer fecha/litros del correo.", file=sys.stderr)
            return 1
        store.upsert_recoleccion(row)
        print(f"recoleccion {row['fecha']}  {row['litros']} L")
    if args.planilla:
        cab, dias = planilla_calidad.parse(args.planilla)
        store.upsert_calidad(cab, dias)
        print(
            f"calidad {cab.get('periodo_desde')}–{cab.get('periodo_hasta')}  "
            f"prot={cab.get('proteina_pct')}  ufc={cab.get('ufc_x1000')}  dias={len(dias)}"
        )
    if args.pesaje:
        n = 0
        for row in pesaje_semanal.parse(args.pesaje):
            store.upsert_pesaje(row)
            n += 1
        print(f"pesaje {n} filas")
    if args.potreros:
        n = 0
        for row in potreros_csv.parse(args.potreros):
            sid = store.ensure_sitio(row["sitio"])
            store.upsert_potrero(sid, row["numero"], row["nombre"], row["geojson"])
            n += 1
        print(f"potreros {n}")
    if args.potreros_xlsx:
        n = 0
        for row in potreros_xlsx.parse(args.potreros_xlsx):
            sid = store.ensure_sitio(row["sitio"])
            store.upsert_potrero(sid, row["numero"], row["nombre"], row["geojson"])
            n += 1
        print(f"potreros xlsx {n}")
    if args.ocr_pesaje:
        rows = ocr_pesaje.parse(args.ocr_pesaje, fecha_default=args.ocr_fecha)
        for row in rows:
            store.upsert_pesaje(row)
        print(f"ocr pesaje {len(rows)} filas")
        if not rows:
            print("OCR no sacó filas. Revisa la foto o pasa --ocr-fecha YYYY-MM-DD.")
    if args.imap:
        from app.imap_acopio import fetch

        return fetch(store, delete_ok=not args.imap_keep, dry=args.dry_run)
    if args.mensaje:
        parsed = mensaje_pastoreo.parse(args.mensaje)
        sid = store.ensure_sitio(args.sitio)
        if parsed["kind"] == "fertilizacion":
            pot = store.find_potrero(sid, parsed.get("potrero") or "")
            if not pot or parsed.get("needs_clarification"):
                print("CLARIFICAR fertilización:", parsed)
                return 3
            store.add_fertilizacion(
                pot["id"], parsed["fecha"], parsed.get("abono"), parsed.get("bultos"), parsed["raw"]
            )
            print(f"fertilizacion {parsed['fecha']} potrero {pot['nombre']} {parsed.get('bultos')} bultos")
        else:
            unclear = parsed.get("needs_clarification")
            if parsed.get("salida"):
                pot = store.find_potrero(sid, parsed["salida"])
                if not pot:
                    print("CLARIFICAR salida:", parsed["salida"])
                    unclear = True
                else:
                    store.add_movimiento(
                        pot["id"], parsed["fecha"], parsed.get("momento"), "salida", parsed["raw"]
                    )
                    print(f"salida {parsed['fecha']} {pot['nombre']}")
            if parsed.get("entrada"):
                pot = store.find_potrero(sid, parsed["entrada"])
                if not pot:
                    print("CLARIFICAR entrada:", parsed["entrada"])
                    unclear = True
                else:
                    store.add_movimiento(
                        pot["id"], parsed["fecha"], parsed.get("momento"), "entrada", parsed["raw"]
                    )
                    print(f"entrada {parsed['fecha']} {pot['nombre']}")
            if unclear:
                return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
