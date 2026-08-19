"""Valores globales. Cada plugin puede sobreescribirlos con plugin_params."""

DEFAULT_VALUES = {
    "pipeline_plugin": "default",
    "web_plugin": "adminlte",
    "load_config": "examples/config/leche_default.json",
    "save_config": "config_out.json",
    "tb_url": "http://127.0.0.1:8080",
    "tb_username": "tenant@thingsboard.org",
    "tb_password": "tenant",
    "web_host": "127.0.0.1",
    "web_port": 5000,
}
