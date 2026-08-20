# Hermes y este repo

Hermes (OpenCode / Telegram / WhatsApp) **no se reescribe aquí**.
Trae el texto (correo, PDF, mensaje del grupo) y llama a data-logger:

```bash
PYTHONPATH=. python3 -m app.ingest --email /tmp/acopio.txt
PYTHONPATH=. python3 -m app.ingest --planilla /tmp/liq.pdf
PYTHONPATH=. python3 -m app.ingest --imap          # buzón .env
PYTHONPATH=. python3 -m app.telegram_pastoreo      # grupo de potreros
```

Acopio y calidad van a SQLite (`data/app.db`), no a ThingsBoard.
Los litros también se pueden POSTEar a TB si un dashboard de TB los
quiere; no es obligatorio.

WhatsApp: el mismo `--mensaje` / parser de pastoreo. El puente nativo
de este repo es Telegram (`app/telegram_pastoreo.py`). WhatsApp lo
sigue cubriendo Hermes si ya está conectado allí.
