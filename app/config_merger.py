"""Precedencia: plugin_params → defaults → archivo JSON → flags --largos."""
from __future__ import annotations

import sys
from typing import Any


def convert_type(value: str) -> Any:
    if value.lower() in ("true", "false"):
        return value.lower() == "true"
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


def merge_config(
    defaults: dict,
    plugin_param_maps: list[dict],
    file_config: dict,
    cli_args: dict,
) -> dict:
    merged: dict = {}
    for params in plugin_param_maps:
        merged.update(params or {})
    merged.update(defaults or {})
    merged.update(file_config or {})
    flags = [a.lstrip("-") for a in sys.argv if a.startswith("--")]
    for key in flags:
        if key in cli_args and cli_args[key] is not None:
            merged[key] = cli_args[key]
    return merged
