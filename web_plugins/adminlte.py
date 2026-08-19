"""Plugin web AdminLTE: Producción, Clima, Calidad."""
from __future__ import annotations

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

from flask import Flask, abort, render_template, request

from app.roles import ROLES, can
from app.store import Store
from tb_client import ThingsBoard


class Plugin:
    plugin_params = {
        "web_host": "127.0.0.1",
        "web_port": 5000,
        "tb_url": "http://127.0.0.1:8080",
        "tb_username": "tenant@thingsboard.org",
        "tb_password": "tenant",
        "device_rain": "lluvia-01",
        "device_clima": "lluvia-01",
        "device_tanque": "",
        "calidad_keys": ["bacterias", "celulas_somaticas", "grasa", "proteina"],
        "calidad_alerts": [
            {
                "key": "bacterias",
                "label": "Bacterias",
                "higher_is_worse": True,
                "min_delta": 0.0,
            }
        ],
        "site_name": "Sitio demo",
        "app_db": "data/app.db",
        "current_role": "admin",
        "current_user": "admin-local",
    }

    def __init__(self) -> None:
        self.params = dict(self.plugin_params)
        self._tb: ThingsBoard | None = None
        self._store: Store | None = None

    def set_params(self, **kwargs) -> None:
        self.params.update(kwargs)

    def store(self) -> Store:
        if self._store is None:
            self._store = Store(self.params.get("app_db") or "data/app.db")
        return self._store

    def _client(self) -> ThingsBoard | None:
        if self._tb and self._tb.token:
            return self._tb
        try:
            tb = ThingsBoard(self.params["tb_url"])
            tb.login(self.params["tb_username"], self.params["tb_password"])
            self._tb = tb
            return tb
        except Exception:
            self._tb = None
            return None

    def _device(self, name: str) -> dict | None:
        if not name:
            return None
        tb = self._client()
        if not tb:
            return None
        try:
            return tb.find_device_by_name(name)
        except Exception:
            return None

    def _latest(self, device_name: str, keys: list[str]) -> dict:
        dev = self._device(device_name)
        if not dev:
            return {}
        try:
            raw = self._client().latest_timeseries(dev["id"]["id"], keys)
        except Exception:
            return {}
        out = {}
        for k, series in (raw or {}).items():
            if series:
                out[k] = series[0]
        return out

    def _history(self, device_name: str, keys: list[str], hours: int = 48) -> dict:
        dev = self._device(device_name)
        if not dev:
            return {}
        end = int(time.time() * 1000)
        start = end - hours * 3600 * 1000
        try:
            return self._client().timeseries(dev["id"]["id"], keys, start, end) or {}
        except Exception:
            return {}

    def _pressure_hint(self, history: dict) -> str:
        pts = history.get("pressure") or []
        if len(pts) < 2:
            return "Sin serie de presión todavía (BME280 en el ESP32)."
        first = float(pts[0]["value"])
        last = float(pts[-1]["value"])
        delta = last - first
        if delta <= -1.5:
            return (
                f"Presión bajó {abs(delta):.1f} hPa en la ventana. "
                "En campo eso suele ir con cielo cerrado y menos viento: más chance de lluvia."
            )
        if delta >= 1.5:
            return (
                f"Presión subió {delta:.1f} hPa. "
                "Suele acompañar aire más seco; menos chance de lluvia inmediata."
            )
        return f"Presión estable ({delta:+.1f} hPa). Ni aviso ni despeje claro."

    def _calidad_rows(self) -> tuple[list[dict], list[dict], dict, dict | None]:
        last = self.store().last_calidad()
        series = self.store().calidad_series()
        hist: dict = {
            "proteina_pct": [{"ts": r["periodo_hasta"], "value": r["proteina_pct"]} for r in series if r.get("proteina_pct") is not None],
            "grasa_pct": [{"ts": r["periodo_hasta"], "value": r["grasa_pct"]} for r in series if r.get("grasa_pct") is not None],
            "ufc_x1000": [{"ts": r["periodo_hasta"], "value": r["ufc_x1000"]} for r in series if r.get("ufc_x1000") is not None],
        }
        alerts = []
        ufc_pts = [r["ufc_x1000"] for r in series if r.get("ufc_x1000") is not None]
        if len(ufc_pts) >= 2 and ufc_pts[-1] > ufc_pts[0]:
            alerts.append(
                {
                    "label": "UFC ×1000/ml",
                    "ok": False,
                    "text": f"Subió de {ufc_pts[0]} a {ufc_pts[-1]} — vigilar higiene.",
                }
            )
        elif last and last.get("ufc_x1000") is not None:
            alerts.append(
                {
                    "label": "UFC ×1000/ml",
                    "ok": True,
                    "text": f"Último {last['ufc_x1000']} (promedio de la liquidación).",
                }
            )
        rows = []
        if last:
            for k, label in (
                ("proteina_pct", "Proteína %"),
                ("grasa_pct", "Grasa %"),
                ("solidos_pct", "Sólidos %"),
                ("ufc_x1000", "UFC ×1000/ml"),
                ("precio_final_litro", "Precio $/L"),
            ):
                rows.append({"key": label, "value": last.get(k), "ts": last.get("periodo_hasta")})
        return rows, alerts, hist, last

    def serve(self) -> None:
        tmpl = str(Path(__file__).resolve().parent / "templates")
        app = Flask(__name__, template_folder=tmpl)
        plugin = self

        def role() -> str:
            r = request.args.get("rol") or plugin.params.get("current_role") or "operario"
            return r if r in ROLES else "operario"

        def require(module: str) -> None:
            if not can(role(), module):
                abort(403)

        def sitio_id() -> int | None:
            sitios = plugin.store().sitios_de(
                None if role() == "admin" else plugin.params.get("current_user")
            )
            if request.args.get("sitio_id"):
                return int(request.args["sitio_id"])
            return sitios[0]["id"] if sitios else None

        @app.context_processor
        def inject():
            r = role()
            return {
                "site_name": plugin.params.get("site_name") or "data-logger",
                "tb_ok": plugin._client() is not None,
                "role": r,
                "role_label": ROLES[r]["label"],
                "modules": ROLES[r]["modules"],
                "sitios": plugin.store().sitios_de(
                    None if r == "admin" else plugin.params.get("current_user")
                ),
                "sitio_id": sitio_id(),
            }

        @app.errorhandler(403)
        def forbidden(_e):
            return render_template("forbidden.html"), 403

        @app.route("/")
        def home():
            return render_template("index.html")

        @app.route("/produccion")
        def produccion():
            require("produccion")
            tank = plugin._latest(
                plugin.params.get("device_tanque") or "",
                ["level_mm", "temperature"],
            )
            rec = plugin.store().last_recoleccion()
            pesaje = plugin.store().pesaje_ultimo_dia()
            return render_template(
                "produccion.html",
                tank=tank,
                rec=rec,
                pesaje=pesaje,
            )

        @app.route("/clima")
        def clima():
            require("clima")
            keys = ["rain_mm", "temperature", "humidity", "pressure", "tips_day"]
            rain_dev = plugin.params.get("device_rain") or ""
            clima_dev = plugin.params.get("device_clima") or rain_dev
            latest = {}
            latest.update(plugin._latest(clima_dev, keys))
            latest.update(plugin._latest(rain_dev, ["rain_mm", "tips_day"]))
            hist = plugin._history(clima_dev, ["pressure", "temperature", "humidity"], 48)
            rain_hist = plugin._history(rain_dev, ["rain_mm"], 48 * 3)
            return render_template(
                "clima.html",
                latest=latest,
                hint=plugin._pressure_hint(hist),
                hist=hist,
                rain_hist=rain_hist,
            )

        @app.route("/calidad")
        def calidad():
            require("calidad")
            rows, alerts, hist, last = plugin._calidad_rows()
            return render_template(
                "calidad.html", rows=rows, alerts=alerts, hist=hist, last=last
            )

        @app.route("/pastoreo")
        def pastoreo():
            require("pastoreo")
            sid = sitio_id()
            return render_template("pastoreo.html", sitio_id=sid or 0)

        @app.route("/api/pastoreo")
        def api_pastoreo():
            require("pastoreo")
            sid = sitio_id()
            if not sid:
                return {"potreros": [], "ocupacion": None}
            pots = []
            for p in plugin.store().potreros(sid):
                item = dict(p)
                item["movimientos"] = plugin.store().historial_potrero(p["id"], 5)
                item["fertilizaciones"] = plugin.store().fertilizaciones_potrero(p["id"], 5)
                pots.append(item)
            return {"potreros": pots, "ocupacion": plugin.store().ocupacion(sid)}

        @app.route("/accounting")
        def accounting():
            require("accounting")
            return render_template("admin_stub.html", heading="Accounting")

        @app.route("/authorization")
        def authorization():
            require("authorization")
            return render_template("admin_stub.html", heading="Authorization")

        @app.route("/users")
        def users():
            require("users")
            return render_template("admin_stub.html", heading="Usuarios")

        host = self.params.get("web_host") or "127.0.0.1"
        port = int(self.params.get("web_port") or 5000)
        print(f"Web en http://{host}:{port}/  rol={self.params.get('current_role')}")
        app.run(host=host, port=port, debug=False)
