#!/usr/bin/env python3
"""Punto de entrada: fusiona config, carga el pipeline y lo corre."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

from app.config import DEFAULT_VALUES
from app.config_merger import merge_config
from app.plugin_loader import get_plugin_params, load_plugin


def _load_json(path: str | None) -> dict:
    if not path:
        return {}
    p = Path(path)
    if not p.is_file():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="data-logger — pipeline de telemetría")
    p.add_argument("--load_config", default=DEFAULT_VALUES["load_config"])
    p.add_argument("--save_config", default=DEFAULT_VALUES["save_config"])
    p.add_argument("--pipeline_plugin", default=None)
    p.add_argument("--web_plugin", default=None)
    p.add_argument("--tb_url", default=None)
    p.add_argument("--web_host", default=None)
    p.add_argument("--web_port", type=int, default=None)
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    file_cfg = _load_json(args.load_config)
    pipe_name = args.pipeline_plugin or file_cfg.get("pipeline_plugin") or DEFAULT_VALUES["pipeline_plugin"]
    web_name = args.web_plugin or file_cfg.get("web_plugin") or DEFAULT_VALUES["web_plugin"]

    pipe_params = get_plugin_params("pipeline.plugins", pipe_name)
    web_params = get_plugin_params("web.plugins", web_name)
    # Bloque plugins.<tipo> del JSON sobreescribe solo esas claves.
    file_flat = {k: v for k, v in file_cfg.items() if k != "plugins"}
    extra = {}
    for section in (file_cfg.get("plugins") or {}).values():
        if isinstance(section, dict):
            extra.update(section)
    file_flat.update(extra)

    cfg = merge_config(
        DEFAULT_VALUES,
        [pipe_params, web_params],
        file_flat,
        vars(args),
    )
    cfg["pipeline_plugin"] = pipe_name
    cfg["web_plugin"] = web_name

    out = Path(cfg.get("save_config") or "config_out.json")
    out.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")

    pipe_cls, _ = load_plugin("pipeline.plugins", pipe_name)
    pipeline = pipe_cls()
    pipeline.set_params(**cfg)
    pipeline.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
