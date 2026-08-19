"""Roles de la app (humanos). No son los tokens de los ESP32."""

# admin: todo.
# veterinario: operación completa; no ve otros usuarios, ni accounting, ni authorization.
# operario: solo lectura; clima, producción y pastoreo; sin calidad.
ROLES = {
    "admin": {
        "label": "Administrador",
        "modules": {
            "produccion",
            "clima",
            "calidad",
            "pastoreo",
            "accounting",
            "authorization",
            "users",
        },
        "write": True,
    },
    "veterinario": {
        "label": "Veterinario",
        "modules": {"produccion", "clima", "calidad", "pastoreo"},
        "write": True,
    },
    "operario": {
        "label": "Operario",
        "modules": {"produccion", "clima", "pastoreo"},
        "write": False,
    },
}


def can(role: str, module: str) -> bool:
    spec = ROLES.get(role) or ROLES["operario"]
    return module in spec["modules"]


def can_write(role: str) -> bool:
    spec = ROLES.get(role) or ROLES["operario"]
    return bool(spec["write"])
