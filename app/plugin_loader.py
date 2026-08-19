"""Carga plugins por entry points, con fallback a import de disco."""
from __future__ import annotations

import importlib
from typing import Any

FALLBACK = {
    ("pipeline.plugins", "default"): "pipeline_plugins.default:PipelinePlugin",
    ("web.plugins", "adminlte"): "web_plugins.adminlte:Plugin",
}


def _from_path(dotted: str) -> Any:
    mod_name, _, cls_name = dotted.partition(":")
    return getattr(importlib.import_module(mod_name), cls_name)


def load_plugin(plugin_group: str, plugin_name: str):
    try:
        from importlib.metadata import entry_points

        group = entry_points().select(group=plugin_group)
        ep = next(ep for ep in group if ep.name == plugin_name)
        plugin_class = ep.load()
    except Exception:
        key = (plugin_group, plugin_name)
        if key not in FALLBACK:
            raise ImportError(f"Plugin {plugin_name} no está en {plugin_group}.")
        plugin_class = _from_path(FALLBACK[key])
    params = dict(getattr(plugin_class, "plugin_params", {}) or {})
    return plugin_class, list(params.keys())


def get_plugin_params(plugin_group: str, plugin_name: str) -> dict:
    cls, _ = load_plugin(plugin_group, plugin_name)
    return dict(getattr(cls, "plugin_params", {}) or {})
