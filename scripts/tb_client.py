"""Cliente mínimo de ThingsBoard (stdlib only)."""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent


def load_env() -> dict[str, str]:
    env = {
        "TB_URL": "http://127.0.0.1:8080",
        "TB_TENANT_EMAIL": "tenant@thingsboard.org",
        "TB_TENANT_PASSWORD": "tenant",
        "TB_HTTP_PORT": "8080",
    }
    env_path = ROOT / ".env"
    if env_path.exists():
        for raw in env_path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            env[key.strip()] = value.strip()
    # Variables reales del proceso ganan.
    for key in list(env):
        if key in os.environ:
            env[key] = os.environ[key]
    return env


def tb_url(env: dict[str, str] | None = None) -> str:
    env = env or load_env()
    return env["TB_URL"].rstrip("/")


class ThingsBoard:
    def __init__(self, base_url: str, token: str | None = None) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token

    def _request(
        self,
        method: str,
        path: str,
        body: Any | None = None,
        auth: bool = True,
    ) -> Any:
        data = None
        headers = {"Accept": "application/json"}
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        if auth:
            if not self.token:
                raise RuntimeError("No hay token JWT. Llama login() primero.")
            headers["X-Authorization"] = f"Bearer {self.token}"
        req = urllib.request.Request(
            f"{self.base_url}{path}",
            data=data,
            headers=headers,
            method=method,
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read()
                if not raw:
                    return None
                return json.loads(raw.decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"{method} {path} → HTTP {exc.code}: {detail}") from exc

    def login(self, username: str, password: str) -> str:
        payload = self._request(
            "POST",
            "/api/auth/login",
            {"username": username, "password": password},
            auth=False,
        )
        self.token = payload["token"]
        return self.token

    def get(self, path: str) -> Any:
        return self._request("GET", path)

    def post(self, path: str, body: Any | None = None) -> Any:
        return self._request("POST", path, body)

    def find_customer_by_title(self, title: str) -> dict[str, Any] | None:
        page = self.get(f"/api/customers?pageSize=100&page=0&textSearch={urllib.parse.quote(title)}")
        for item in page.get("data", []):
            if item.get("title") == title:
                return item
        return None

    def ensure_customer(self, title: str) -> dict[str, Any]:
        existing = self.find_customer_by_title(title)
        if existing:
            return existing
        return self.post("/api/customer", {"title": title})

    def find_device_by_name(self, name: str) -> dict[str, Any] | None:
        # Búsqueda de tenant (no filtra por customer).
        page = self.get(
            f"/api/tenant/devices?pageSize=100&page=0&textSearch={urllib.parse.quote(name)}"
        )
        for item in page.get("data", []):
            if item.get("name") == name:
                return item
        return None

    def ensure_device(
        self,
        name: str,
        device_type: str,
        label: str,
        customer_id: str | None = None,
    ) -> dict[str, Any]:
        existing = self.find_device_by_name(name)
        if existing:
            device = existing
        else:
            device = self.post(
                "/api/device",
                {"name": name, "type": device_type, "label": label},
            )
        if customer_id:
            self.post(f"/api/customer/{customer_id}/device/{device['id']['id']}")
            device = self.get(f"/api/device/{device['id']['id']}")
        return device

    def create_customer_user(
        self,
        customer_id: str,
        email: str,
        password: str,
        first_name: str = "",
    ) -> dict[str, Any]:
        """Crea un CUSTOMER_USER. La API de credenciales varía; si falla, click-ops."""
        user = self.post(
            "/api/user?sendActivationMail=false",
            {
                "email": email,
                "authority": "CUSTOMER_USER",
                "firstName": first_name or email.split("@")[0],
                "lastName": "",
                "customerId": {"entityType": "CUSTOMER", "id": customer_id},
            },
        )
        uid = user["id"]["id"]
        try:
            self.post(
                f"/api/user/{uid}/userCredentials",
                {"enabled": True, "password": password},
            )
        except RuntimeError as exc:
            print(
                f"AVISO: usuario {email} creado pero la clave hay que "
                f"activarla en la UI (Users). Detalle: {exc}"
            )
        return user

    def latest_timeseries(self, device_id: str, keys: list[str]) -> dict:
        q = urllib.parse.quote(",".join(keys))
        return self.get(
            f"/api/plugins/telemetry/DEVICE/{device_id}/values/timeseries?keys={q}"
        ) or {}

    def timeseries(
        self,
        device_id: str,
        keys: list[str],
        start_ts: int,
        end_ts: int,
        limit: int = 200,
    ) -> dict:
        q = urllib.parse.urlencode(
            {
                "keys": ",".join(keys),
                "startTs": start_ts,
                "endTs": end_ts,
                "limit": limit,
                "agg": "NONE",
            }
        )
        return self.get(
            f"/api/plugins/telemetry/DEVICE/{device_id}/values/timeseries?{q}"
        ) or {}

    def device_token(self, device_id: str) -> str:
        creds = self.get(f"/api/device/{device_id}/credentials")
        token = creds.get("credentialsId")
        if not token:
            raise RuntimeError(f"El dispositivo {device_id} no tiene access token.")
        return token


def post_telemetry(base_url: str, access_token: str, payload: dict[str, Any]) -> int:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{base_url.rstrip('/')}/api/v1/{access_token}/telemetry",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.status


def post_attributes(base_url: str, access_token: str, payload: dict[str, Any]) -> int:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{base_url.rstrip('/')}/api/v1/{access_token}/attributes",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.status
