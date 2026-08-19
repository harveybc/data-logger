# Prompt — implementar el puente Telegram → ingest (P2/P3)

El repo **aún no tiene** este archivo. Este prompt es para que un
agente lo escriba. No pongas el token en el código.

---

Lee `docs/AGENTES.md` (P2, P3, P4, P5), `docs/PASTOREO.md`,
`ingest_plugins/mensaje_pastoreo.py` y `app/store.py`.

Implementa `app/telegram_pastoreo.py` (stdlib + `http.client` o una
lib mínima que declares en `requirements.txt`):

- Lee `TELEGRAM_BOT_TOKEN` y `TELEGRAM_CHAT_ID` de `.env`.
- Long-poll `getUpdates`. Solo ese chat_id.
- Cada texto: `mensaje_pastoreo.parse`.
- Si `needs_clarification` o `find_potrero` falla: responde en el chat
  pidiendo corrección y lista numero+nombre de potreros del `--sitio`
  (env `PASTOREO_SITIO`).
- Si está claro: `Store.add_movimiento` / `add_fertilizacion` (o
  subprocess a `python3 -m app.ingest --mensaje`).
- No respondas a stickers ni a “ok”.
- Documenta en `docs/AGENTES.md` cómo arrancar:
  `PYTHONPATH=. python3 -m app.telegram_pastoreo`
- Añade `.env.example` con las claves **vacías**.

No crees el bot en BotFather tú. Yo pongo el token.

---
