"""Pipeline por defecto: carga el plugin web y lo sirve."""
from __future__ import annotations

from app.plugin_loader import load_plugin


class PipelinePlugin:
    plugin_params = {
        "web_plugin": "adminlte",
        "web_host": "127.0.0.1",
        "web_port": 5000,
    }

    def __init__(self) -> None:
        self.params = dict(self.plugin_params)

    def set_params(self, **kwargs) -> None:
        self.params.update(kwargs)

    def run(self) -> None:
        name = self.params.get("web_plugin") or "adminlte"
        web_cls, _ = load_plugin("web.plugins", name)
        web = web_cls()
        web.set_params(**self.params)
        web.serve()
