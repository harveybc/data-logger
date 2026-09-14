# Plugin agro (primer dominio, no el core)

`web_plugins.adminlte` + `ingest_plugins.email_recoleccion` + IMAP.
Harvey es **alpha tester indoor**. El core (`data-logger`) no es una
app de finca.

## Alcance ahora vs después

| Ahora | Después (no implementar hasta que el plot diario funcione) |
|---|---|
| Correo de **recolección** (planta, ~1 día tarde) → fecha + litros | Calidad quincenal (web, vet/admin; **nunca** al chat) |
| Curva L/día en `/produccion` | WhatsApp **silencioso** en **un** grupo existente (solo “ayer: N L”) |
| IMAP a un buzón **nuevo** | Mapa de potreros, rotación, fertilización |
| | Foto manuscrita por vaca (OCR al final) |

WhatsApp: el agente **no** habla, **no** alerta, **no** entra a otros
grupos. Un intento anterior mandó mensajes a todos los chats: eso es
config mala. Cuando toque: un `chat_id` fijo, `send=false` por defecto,
allowlist de un grupo. Hoy **no** se configura WhatsApp.

## Buzón: dónde abrirlo

**Gmail nuevo, solo para acopio.** No Proton, no Outlook, no el Gmail
personal.

Motivo: el correo de la planta ya llega a Gmail; el filtro
Gmail→Gmail + IMAP + contraseña de aplicación es el camino que no
rompe. Proton/IMAP de terceros pelea con el reenvío de Google.

Nombre sugerido: `acopio.datalogger.<algo>@gmail.com` (sin tu nombre
real en el local-part si puedes).

Pasos (los haces **tú**):

1. Crear esa cuenta. No es la personal.
2. 2FA + [contraseña de aplicación](https://myaccount.google.com/apppasswords) “Correo”.
3. Ajustes → Reenvío y POP/IMAP → **habilitar IMAP**.
4. En el Gmail **personal** (donde llega Colácteos / la planta):
   filtro *Asunto contiene* `Recolección de leche` (ajusta si el asunto
   real es otro) → **Reenviar** al buzón nuevo. Google pide confirmar
   el reenvío una vez.
5. **No** des al agente la contraseña de la cuenta personal.
6. En el checkout:

```bash
cd data-logger
cp -n .env.example .env
# IMAP_USER=acopio.datalogger....@gmail.com
# IMAP_PASSWORD=xxxx xxxx xxxx xxxx   # 16 caracteres, no la clave de login
PYTHONPATH=. python3 -m app.ingest --imap --dry-run
```

`--dry-run` lista. Sin él, escribe `data/app.db` y **borra el mensaje
solo del buzón nuevo** cuando el parseo y el upsert salieron bien.
Si el parseo falla, el correo se queda.

Cron (el envío a veces se retrasa un día):

```
0 */6 * * * cd /ruta/data-logger && PYTHONPATH=. python3 -m app.ingest --imap >> data/imap.log 2>&1
```

El chat de trabajadores **no** recibe esto. La web sí (fecha, litros,
histórico).

## Qué necesito de Harvey para arrancar

1. Buzón creado + IMAP on + app password (me la pasas por un canal
   privado, **nunca** en git ni en el README).
2. Confirmación de que el filtro de reenvío ya está y Google lo aceptó.
3. **Un correo real de recolección**, reenviado o `.eml` / texto, con
   cédulas/NIT tapados. El fixture `examples/fixtures/recoleccion_email.txt`
   es demo. Si el asunto o las etiquetas (`Fecha`, `Litros`) cambian, el
   parser hay que ajustarlo **con ese texto**, no a ojo.
4. Nombre del sitio en el JSON (`leche_default.json`) como lo quieres
   ver en el menú.
5. En qué máquina corre el cron (omega u otra). No parar GPU/Postgres
   ajenos.

No hace falta WhatsApp, BotFather, Excel de potreros ni fotos de vacas
para este primer plot.

## Pegar a un agente (este plugin)

> Estás en `data-logger`. El **core** no es agro. El trabajo es el
> **plugin agro**, solo acopio diario. Lee `docs/plugins/agro.md` y
> `AGENTS.md`. No configures WhatsApp. No envíes mensajes a ningún
> chat. No uses la cuenta de Gmail personal. Con `.env` IMAP del
> buzón nuevo: `PYTHONPATH=. python3 -m app.ingest --imap --dry-run`,
> enseña cuántos mensajes vio y si parseó Fecha/Litros. Si dry-run
> está bien, corre sin `--dry-run` una vez. Arranca
> `PYTHONPATH=. python3 -m app.main --load_config examples/config/leche_default.json`
> y dime http://127.0.0.1:5000/produccion. No detengas Docker que no
> hayas levantado tú.

## Código ya existente

| Pieza | Dónde |
|---|---|
| Parser | `ingest_plugins/email_recoleccion.py` |
| IMAP | `app/imap_acopio.py` |
| CLI | `python3 -m app.ingest --imap` / `--email` |
| UI + plot | `/produccion` (`web_plugins/templates/produccion.html`) |

Lo que **no** está hecho: el buzón real, el filtro de reenvío, y
WhatsApp. El plot aparece en cuanto haya filas en `recoleccion`.
