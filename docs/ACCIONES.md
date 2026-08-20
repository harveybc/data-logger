# Lo que tienes que hacer tú (el código ya está)

Prioridad: **correo de acopio**. El hardware puede tardar; esto no.

## 1. Buzón nuevo (hoy / esta semana)

1. Crea un Gmail **solo** para la planta (no el personal).
2. Activa la verificación en 2 pasos.
3. [Contraseñas de aplicación](https://myaccount.google.com/apppasswords) →
   genera una para “Correo”. Cópiala a `.env` como `IMAP_PASSWORD`.
4. En Gmail: Ajustes → Reenvío y correo POP/IMAP → **Habilitar IMAP**.
5. En la cuenta **personal** (donde llega Colácteos):
   Filtro: Asunto contiene `Recolección de leche` →
   Reenviar a la cuenta nueva.
   (Gmail pide confirmar el reenvío una vez.)
6. En el checkout:

```bash
cd data-logger
cp -n .env.example .env
# edita IMAP_USER=el-buzon-nuevo@gmail.com
#        IMAP_PASSWORD=xxxx xxxx xxxx xxxx
PYTHONPATH=. python3 -m app.ingest --imap --dry-run
```

Si `--dry-run` lista los correos bien, quita `--dry-run`. El script
**borra el mensaje del buzón solo después** de escribir en
`data/app.db`. Si el parseo falla, el correo se queda.

Cron (cada 6 h, por si un envío se retrasa):

```
0 */6 * * * cd /ruta/data-logger && PYTHONPATH=. python3 -m app.ingest --imap >> data/imap.log 2>&1
```

## 2. Telegram de potreros (cuando quieras el grupo en vivo)

1. Telegram → `@BotFather` → `/newbot` → `TELEGRAM_BOT_TOKEN` en `.env`.
2. Añade el bot al grupo de trabajo (o úsalo 1:1).
3. Escribe un mensaje, luego visita
   `https://api.telegram.org/bot<TOKEN>/getUpdates` y copia el
   `chat.id` a `TELEGRAM_CHAT_ID`.
4. `PASTOREO_SITIO=` el nombre del predio (el de `--potreros`).
5. `PYTHONPATH=. python3 -m app.telegram_pastoreo`

WhatsApp: si Hermes ya lee ese chat, que ejecute el mismo
`--mensaje`. Aquí no hay API oficial de WhatsApp.

## 3. Excel de potreros

Cuando lo encuentres:

```bash
PYTHONPATH=. python3 -m app.ingest --potreros-xlsx /ruta/potreros.xlsx
```

Columnas aceptadas: `sitio`, `numero`/`nro`/`id`, `nombre`,
`geojson` o `wkt`. `pip install openpyxl` una vez.

## 4. Foto del pesaje (lunes/martes)

```bash
sudo apt install tesseract-ocr tesseract-ocr-spa
PYTHONPATH=. python3 -m app.ingest --ocr-pesaje /ruta/foto.jpg --ocr-fecha 2026-08-18
```

Revisa las filas en Producción. El OCR de letra a mano falla: si
sale basura, pasa un CSV.

## 5. No hace falta para el IMAP

- Hardware / ESP32 (cuando llegue Amazon).
- Google login / Mercado Pago.
- Borrar nada a mano en la bandeja personal: el filtro reenvía; el
  script limpia **solo** el buzón nuevo.
