# Agro dashboard plugin (example)

Example **domain** plugin on `data-logger`: AdminLTE menus for production,
climate, quality and grazing, plus ingest of plant emails, quality PDFs
and paddock messages.

Copy this pattern for another dashboard (house climate, lab, …): a
`web_plugins` module, a JSON block, ingest plugins if you have documents,
not a fork of the core.

Config: `examples/config/leche_default.json`.

```bash
pip install -r requirements.txt
PYTHONPATH=. python3 -m app.main --load_config examples/config/leche_default.json
```

UI: **http://127.0.0.1:5000**

| Path | What |
|---|---|
| `/produccion` | Last pickup (date, litres) and history chart |
| `/clima` | ThingsBoard climate series |
| `/calidad` | Fortnightly quality (web only) |
| `/pastoreo` | Paddock moves |

Demo roles: `?rol=admin`, `veterinario`, `operario` (read-only, no quality).

## Ingest

```bash
PYTHONPATH=. python3 -m app.ingest --imap          # mailbox in .env
PYTHONPATH=. python3 -m app.ingest --email examples/fixtures/recoleccion_email.txt
PYTHONPATH=. python3 -m app.ingest --pesaje examples/fixtures/pesaje_semanal.csv
PYTHONPATH=. python3 -m app.ingest --planilla /path/liquidacion.pdf
PYTHONPATH=. python3 -m app.telegram_pastoreo      # later; not WhatsApp
```

Mailbox, filters, what Harvey must supply: [ACCIONES.md](../../ACCIONES.md).

## Scope now vs later

| Now | Later (not before daily litres plot works) |
|---|---|
| Plant **pickup** email (~1 day late) → date + litres | Fortnightly quality on the web only (never in the work chat) |
| L/day chart on `/produccion` | Silent WhatsApp in **one** existing group (“yesterday: N L”) |
| IMAP to a **new** mailbox | Paddock map, rotation, fertilizer |
| | Per-cow photo OCR (last) |

WhatsApp is **off**. When it exists: one `chat_id`, `send=false` by
default. A previous bot posted in every group; that is forbidden.
Workers never see quality/UFC/route in chat.

## Mailbox

**Dedicated mailbox for pickup** (e.g. `data-logger@…`). Not the personal
inbox. Forward from the account that receives Colácteos / plant mail
(filter on `Recolección de leche`).

On Google Workspace / Gmail for that mailbox:

1. Confirm the forwarded messages appear in the **new** inbox (web UI).
2. Settings → Forwarding and POP/IMAP → **Enable IMAP** (POP alone is
   not enough; this code uses IMAP).
3. **2-Step Verification** on, then an
   [App password](https://myaccount.google.com/apppasswords) for Mail.
   The normal login password is **rejected** by IMAP/POP scripts.
4. Put `IMAP_USER` / `IMAP_PASSWORD` (app password) in `.env` (gitignored).

```bash
cp -n .env.example .env
# IMAP_HOST=imap.gmail.com
# IMAP_USER=data-logger@…
# IMAP_PASSWORD=xxxx xxxx xxxx xxxx   # 16-char app password
PYTHONPATH=. python3 -m app.ingest --imap --dry-run
```

Dry-run lists. Without it, writes `data/app.db` and deletes the message
**only on the new mailbox** after a successful upsert. Failed parse:
mail stays.

**Status (ops):** forwarding of pickup mail is confirmed working. IMAP
login still needs a working **app password** before `--imap` succeeds.

```
0 */6 * * * cd /path/data-logger && PYTHONPATH=. python3 -m app.ingest --imap >> data/imap.log 2>&1
```

## Paste this to an agent

> You are in `data-logger`. Work is the **agro plugin** only: daily
> pickup email. Read `docs/plugins/agro/README.md` and `AGENTS.md`.
> Do not configure WhatsApp. Do not send chat messages. Do not use the
> personal Gmail. With `.env` IMAP of the **new** mailbox run
> `PYTHONPATH=. python3 -m app.ingest --imap --dry-run`, report how many
> messages and whether Fecha/Litros parsed. If dry-run is clean, run
> once without `--dry-run`. Start
> `PYTHONPATH=. python3 -m app.main --load_config examples/config/leche_default.json`
> and give me http://127.0.0.1:5000/produccion. Do not stop Docker you
> did not start.

## Code

| Piece | Where |
|---|---|
| Parser | `ingest_plugins/email_recoleccion.py` |
| IMAP | `app/imap_acopio.py` |
| CLI | `python3 -m app.ingest --imap` / `--email` |
| UI + chart | `/produccion` |

Not done until you create the mailbox: live IMAP. WhatsApp is not in
this milestone.
