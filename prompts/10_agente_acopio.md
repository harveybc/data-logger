# Prompt — agente de acopio (correo de la planta)

Copia el recuadro. Un trabajo: pasar el correo a SQLite. No flashees
nada. No subas datos personales a git.

---

En el repo `data-logger` (https://github.com/harveybc/data-logger) tengo
el texto de un correo de recolección de leche. Lee
`docs/DATOS.md`, `docs/AGENTES.md` (H1) e `ingest_plugins/email_recoleccion.py`.

1. Guarda el cuerpo en un archivo **fuera de git** (p. ej. `/tmp/acopio.txt`).
2. Corre `PYTHONPATH=. python3 -m app.ingest --email /tmp/acopio.txt`.
3. Dime fecha, litros y medida de tanque que quedaron, o el error exacto.
4. No inventes litros. Si el parseo falla, muestra el texto que no calzó.

No abras ThingsBoard para esto. El acopio no va a TB.

---
