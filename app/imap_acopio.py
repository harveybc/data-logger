"""Baja correos de acopio por IMAP, registra, borra solo si la BD confirmó.

Tolerante: procesa todos los que haya; uno fallido no frena a los demás.
Reanuda desde la última fecha en `recoleccion` (menos un margen).
"""
from __future__ import annotations

import argparse
import email
import imaplib
import os
import re
import sys
from datetime import datetime, timedelta
from email.header import decode_header
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.store import Store
from ingest_plugins import email_recoleccion, planilla_calidad


class _Strip(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.out: list[str] = []

    def handle_data(self, data: str) -> None:
        self.out.append(data)

    def text(self) -> str:
        return re.sub(r"\s+", " ", "".join(self.out))


def _env(name: str, default: str = "") -> str:
    if name in os.environ and os.environ[name]:
        return os.environ[name]
    env_path = ROOT / ".env"
    if env_path.exists():
        for raw in env_path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if line.startswith(f"{name}="):
                return line.split("=", 1)[1].strip().strip('"')
    return default


def _decode(s) -> str:
    if s is None:
        return ""
    parts = decode_header(s)
    bits = []
    for data, enc in parts:
        if isinstance(data, bytes):
            bits.append(data.decode(enc or "utf-8", errors="replace"))
        else:
            bits.append(data)
    return "".join(bits)


def _body(msg: email.message.Message) -> str:
    texts: list[str] = []
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            if ctype == "text/plain":
                payload = part.get_payload(decode=True) or b""
                texts.append(payload.decode(part.get_content_charset() or "utf-8", errors="replace"))
            elif ctype == "text/html" and not texts:
                payload = part.get_payload(decode=True) or b""
                html = payload.decode(part.get_content_charset() or "utf-8", errors="replace")
                p = _Strip()
                p.feed(html)
                texts.append(p.text())
    else:
        payload = msg.get_payload(decode=True) or b""
        texts.append(payload.decode(msg.get_content_charset() or "utf-8", errors="replace"))
    return "\n".join(texts)


def _pdfs(msg: email.message.Message) -> list[bytes]:
    out = []
    if not msg.is_multipart():
        return out
    for part in msg.walk():
        name = (part.get_filename() or "").lower()
        if part.get_content_type() == "application/pdf" or name.endswith(".pdf"):
            data = part.get_payload(decode=True)
            if data:
                out.append(data)
    return out


def _mid(msg: email.message.Message) -> str:
    return (msg.get("Message-ID") or msg.get("Message-Id") or "").strip() or (
        "no-id-" + (msg.get("Date") or "") + (msg.get("Subject") or "")
    )


def fetch(store: Store, delete_ok: bool, dry: bool) -> int:
    host = _env("IMAP_HOST", "imap.gmail.com")
    user = _env("IMAP_USER")
    password = _env("IMAP_PASSWORD")
    folder = _env("IMAP_FOLDER", "INBOX")
    subject = _env("IMAP_SUBJECT", "Recolecci")
    lookback = int(_env("IMAP_LOOKBACK_DAYS", "30"))
    if not user or not password:
        print("Falta IMAP_USER / IMAP_PASSWORD en .env", file=sys.stderr)
        return 2

    last = store.last_recoleccion_fecha()
    if last:
        since = datetime.strptime(last, "%Y-%m-%d") - timedelta(days=2)
    else:
        since = datetime.utcnow() - timedelta(days=lookback)
    since_s = since.strftime("%d-%b-%Y")

    imap = imaplib.IMAP4_SSL(host)
    imap.login(user, password)
    imap.select(folder)
    criteria = f'(SINCE {since_s} SUBJECT "{subject}")'
    typ, data = imap.search(None, criteria)
    if typ != "OK":
        print("IMAP search falló:", typ, data)
        imap.logout()
        return 1
    ids = data[0].split()
    print(f"IMAP {len(ids)} mensajes desde {since_s} subject~{subject}")

    ok = fail = skip = 0
    for uid in ids:
        typ, raw = imap.fetch(uid, "(RFC822)")
        if typ != "OK" or not raw or not raw[0]:
            fail += 1
            continue
        msg = email.message_from_bytes(raw[0][1])
        mid = _mid(msg)
        if store.already_ingested(mid):
            skip += 1
            if delete_ok and not dry:
                imap.store(uid, "+FLAGS", "\\Deleted")
            continue
        text = _body(msg)
        subj = _decode(msg["Subject"])
        try:
            row = email_recoleccion.parse(text)
        except Exception as exc:
            store.log_ingest(mid, "email", None, "error", str(exc))
            print("parse error", subj, exc)
            fail += 1
            continue
        if not row.get("fecha") or row.get("litros") is None:
            store.log_ingest(mid, "email", None, "error", "sin fecha/litros")
            print("sin fecha/litros:", subj)
            fail += 1
            continue
        if dry:
            print("DRY", row["fecha"], row["litros"], "L")
            ok += 1
            continue
        try:
            store.upsert_recoleccion(row)
            for blob in _pdfs(msg):
                tmp = ROOT / "data" / "_tmp_planilla.pdf"
                tmp.write_bytes(blob)
                try:
                    cab, dias = planilla_calidad.parse(tmp)
                    store.upsert_calidad(cab, dias)
                    print("  adjunto PDF calidad", cab.get("periodo_hasta"))
                except Exception as exc:
                    print("  PDF adjunto no parseado:", exc)
                finally:
                    tmp.unlink(missing_ok=True)
            store.log_ingest(mid, "email", row["fecha"], "ok", subj)
            if delete_ok:
                imap.store(uid, "+FLAGS", "\\Deleted")
            print(f"ok {row['fecha']} {row['litros']} L  {subj!r}")
            ok += 1
        except Exception as exc:
            store.log_ingest(mid, "email", row.get("fecha"), "error", str(exc))
            print("upsert error", exc)
            fail += 1

    if delete_ok and not dry:
        imap.expunge()
    imap.logout()
    print(f"listo ok={ok} fail={fail} skip={skip}")
    if ids and ok == 0 and fail:
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="IMAP acopio → SQLite, borra solo si OK")
    p.add_argument("--db", default="data/app.db")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--keep", action="store_true", help="No borrar aunque esté OK")
    args = p.parse_args(argv)
    return fetch(Store(args.db), delete_ok=not args.keep, dry=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
