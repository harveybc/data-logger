"""Puente Telegram → pastoreo. Token solo en .env. Un chat (grupo o 1:1)."""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.ingest import main as ingest_main
from app.store import Store


def _env(name: str, default: str = "") -> str:
    if os.environ.get(name):
        return os.environ[name]
    env_path = ROOT / ".env"
    if env_path.exists():
        for raw in env_path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if line.startswith(f"{name}="):
                return line.split("=", 1)[1].strip().strip('"')
    return default


def _api(token: str, method: str, **params):
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None}).encode()
    req = urllib.request.Request(url, data=data)
    with urllib.request.urlopen(req, timeout=40) as resp:
        return json.loads(resp.read().decode())


def _send(token: str, chat_id: int, text: str) -> None:
    _api(token, "sendMessage", chat_id=chat_id, text=text[:3500])


def _offset_path() -> Path:
    p = ROOT / "data"
    p.mkdir(exist_ok=True)
    return p / "telegram_offset"


def run() -> int:
    token = _env("TELEGRAM_BOT_TOKEN")
    want_chat = _env("TELEGRAM_CHAT_ID")
    sitio = _env("PASTOREO_SITIO", "Sitio demo")
    if not token:
        print("Falta TELEGRAM_BOT_TOKEN en .env", file=sys.stderr)
        return 2
    store = Store(ROOT / "data" / "app.db")
    off_file = _offset_path()
    offset = int(off_file.read_text()) if off_file.exists() else 0
    print(f"telegram pastoreo sitio={sitio} chat={want_chat or 'cualquiera'}")
    while True:
        try:
            payload = _api(token, "getUpdates", offset=offset, timeout=25)
        except (urllib.error.URLError, TimeoutError) as exc:
            print("poll", exc)
            time.sleep(5)
            continue
        for upd in payload.get("result") or []:
            offset = int(upd["update_id"]) + 1
            off_file.write_text(str(offset))
            msg = upd.get("message") or upd.get("edited_message") or {}
            chat = msg.get("chat") or {}
            chat_id = chat.get("id")
            text = (msg.get("text") or "").strip()
            if not text or not chat_id:
                continue
            if want_chat and str(chat_id) != str(want_chat):
                continue
            if text.startswith("/"):
                if text.startswith("/potreros"):
                    sid = store.ensure_sitio(sitio)
                    pots = store.potreros(sid)
                    lista = ", ".join(f"{p['numero']} {p['nombre']}" for p in pots) or "(vacío)"
                    _send(token, chat_id, lista)
                continue
            code = ingest_main(["--sitio", sitio, "--mensaje", text, "--db", str(ROOT / "data" / "app.db")])
            if code == 3:
                sid = store.ensure_sitio(sitio)
                pots = store.potreros(sid)
                lista = ", ".join(f"{p['numero']} {p['nombre']}" for p in pots) or "(ninguno cargado)"
                _send(token, chat_id, f"¿Cuál potrero? Conozco: {lista}")
            elif code == 0:
                _send(token, chat_id, "ok, registrado")
            else:
                _send(token, chat_id, "no pude registrar; prueba de nuevo o /potreros")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
