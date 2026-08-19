"""Plugin web AdminLTE: Producción, Clima, Calidad."""
from __future__ import annotations

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

from flask import Flask, render_template

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
    }

    def __init__(self) -> None:
        self.params = dict(self.plugin_params)
        self._tb: ThingsBoard | None = None

    def set_params(self, **kwargs) -> None:
        self.params.update(kwargs)

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

    def _calidad_rows(self) -> tuple[list[dict], list[dict], dict]:
        keys = list(self.params.get("calidad_keys") or [])
        hist = self._history(self.params.get("device_clima") or "", keys, hours=24 * 14)
        alerts = []
        for spec in self.params.get("calidad_alerts") or []:
            key = spec.get("key")
            series = hist.get(key) or []
            if len(series) < 3:
                alerts.append(
                    {
                        "label": spec.get("label") or key,
                        "ok": True,
                        "text": "Sin suficientes muestras todavía.",
                    }
                )
                continue
            vals = [float(p["value"]) for p in series[-8:]]
            slope = vals[-1] - vals[0]
            worse = spec.get("higher_is_worse", True)
            min_delta = float(spec.get("min_delta") or 0)
            firing = (slope > min_delta) if worse else (slope < -min_delta)
            alerts.append(
                {
                    "label": spec.get("label") or key,
                    "ok": not firing,
                    "text": f"Δ reciente = {slope:+.2f}"
                    + (" — tendencia a vigilar" if firing else " — estable"),
                }
            )
        rows = []
        # Último valor por clave
        latest = self._latest(self.params.get("device_clima") or "", keys)
        for k in keys:
            cell = latest.get(k) or {}
            rows.append({"key": k, "value": cell.get("value"), "ts": cell.get("ts")})
        return rows, alerts, hist

    def serve(self) -> None:
        tmpl = str(Path(__file__).resolve().parent / "templates")
        app = Flask(__name__, template_folder=tmpl)
        plugin = self

        @app.context_processor
        def inject():
            return {
                "site_name": plugin.params.get("site_name") or "data-logger",
                "tb_ok": plugin._client() is not None,
            }

        @app.route("/")
        def home():
            return render_template("index.html")

        @app.route("/produccion")
        def produccion():
            tank = plugin._latest(
                plugin.params.get("device_tanque") or "",
                ["level_mm", "temperature"],
            )
            return render_template(
                "produccion.html",
                tank=tank,
                hermes_pending=True,
                pesaje_pending=True,
            )

        @app.route("/clima")
        def clima():
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
            rows, alerts, hist = plugin._calidad_rows()
            return render_template("calidad.html", rows=rows, alerts=alerts, hist=hist)

        host = self.params.get("web_host") or "127.0.0.1"
        port = int(self.params.get("web_port") or 5000)
        print(f"Web AdminLTE en http://{host}:{port}/  (Clima / Producción / Calidad)")
        app.run(host=host, port=port, debug=False)
