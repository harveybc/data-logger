# Agentes de automatización — cómo crearlos

Este es el recetario. **Ningún bot se crea solo**: hace falta un token
(Telegram) o una bandeja (correo). El parseo ya existe en este repo;
el agente solo trae el texto y llama a `app.ingest`.

Un agente = **un trabajo**. No mezclar “lee el grupo” con “flashea el
ESP32” en la misma conversación.

Prompts listos para copiar: `prompts/10` … `prompts/16`.

## Mapa

| ID | Agente | Qué mira | Qué escribe | Estado del código |
|---|---|---|---|---|
| **H1** | Acopio diario | Correo de la planta (llega ~1 día tarde) | `python3 -m app.ingest --email ARCHIVO` | Parser hecho |
| **H2** | Calidad / liquidación | PDF de la quincena | `--planilla PDF` | Parser hecho |
| **H3** | Producción por vaca | CSV o foto transcrita | `--pesaje CSV` | Parser hecho |
| **P1** | Carga de potreros | Excel → CSV | `--potreros CSV` | CSV hecho; Excel cuando esté |
| **P2** | Rotación (grupo de trabajo) | Telegram/WhatsApp del predio | `--mensaje "…" --sitio NOMBRE` | Parser hecho; bot **no** |
| **P3** | Rotación (bot dedicado) | Chat 1:1 con el operario | igual que P2 | Igual |
| **P4** | Fertilización | Mismos canales que P2/P3 | mismo `--mensaje` | Mismo parser |
| **P5** | Aclarar nombre de potrero | Respuesta del grupo | reintenta `--mensaje` | Solo imprime `CLARIFICAR` |
| **S1** | Sensores / ThingsBoard | — | no parsea documentos | `prompts/01`–`05` |

Hermes (cuando exista) **es H1+H2**, no un quinto almacén. Llama a
`ingest_plugins.email_recoleccion` / `planilla_calidad`.

## Reglas para no envenenar el desayuno

- No inventar litros, UFC ni potreros. Si no entiende: `CLARIFICAR`.
- No guardar cédulas, NIT ni nombres de personas en git. Fixtures
  anónimos (`examples/fixtures/`).
- No crear el bot de Telegram en el repo con un token real.
- Token del bot y chat_id van en `.env` (gitignorado).
- El agente **no** entra a accounting ni authorization. Eso es admin.
- Sitio (`--sitio`) obligatorio. Un usuario puede tener varios sitios.

## Cómo se crea cada uno

### H1 — Correo de acopio

1. Bandeja que reciba `noresponder@…` de la planta (o reenvío a una
   carpeta). Hermes u otro lector saca el **cuerpo en texto**.
2. Guarda un `.txt` y corre:

```bash
PYTHONPATH=. python3 -m app.ingest --email /ruta/correo.txt
```

3. Prompt: `prompts/10_agente_acopio.md`.

Hasta que Hermes viva, se puede pegar el correo a un agente de código
y pedirle que escriba el `.txt` y ejecute el ingest.

### H2 — PDF de calidad

```bash
PYTHONPATH=. python3 -m app.ingest --planilla /ruta/liquidacion.pdf
```

Hace falta `pdftotext` (poppler) o `pypdf`. Prompt: `prompts/11_agente_calidad.md`.

### H3 — AM/PM por vaca

CSV con cabecera exacta: `fecha,placa,litros_am,litros_pm`.

```bash
PYTHONPATH=. python3 -m app.ingest --pesaje /ruta/semana.csv
```

Prompt: `prompts/12_agente_pesaje.md`.

### P1 — Polígonos

Cuando esté el Excel: exportar CSV `sitio,numero,nombre,geojson`.
GeoJSON = un polígono por fila (coordenadas del predio, **no** GPS del
ESP32).

```bash
PYTHONPATH=. python3 -m app.ingest --potreros /ruta/potreros.csv
```

Prompt: `prompts/13_agente_potreros.md`.

### P2 y P3 — Telegram (grupo o bot dedicado)

Aún **no hay código de bot** en este repo. El contrato es:

1. En Telegram: `@BotFather` → `/newbot` → guardar `TELEGRAM_BOT_TOKEN`
   en `.env`. **Nunca** en git.
2. Grupo de trabajo: añadir el bot, anotar `TELEGRAM_CHAT_ID`.
   Bot dedicado: el operario habla al bot en privado; mismo token,
   otro chat_id.
3. El proceso (cuando se escriba `app/telegram_pastoreo.py`) debe:
   - leer solo mensajes de texto de ese chat;
   - llamar `ingest_plugins.mensaje_pastoreo.parse`;
   - si `needs_clarification` o potrero desconocido: **responder en el
     mismo chat** “¿cuál potrero? Los que conozco: 1 Alto, 2 Vega…”;
   - si está claro: `Store.add_movimiento` / `add_fertilizacion` (o
     `python3 -m app.ingest --mensaje "…" --sitio "NOMBRE"`);
   - no responder a cada “ok” ni a fotos hasta que haya un flujo de
     transcripción.
4. Prompt para que un agente **implemente** ese puente:
   `prompts/14_crear_bot_telegram.md`.
5. Prompt del **alma** que corre 24/7 leyendo el grupo:
   `prompts/15_alma_pastoreo.md`.

P2 y P3 comparten parser. Solo cambia el chat_id.

### P4 — Fertilización

No es otro bot. El mismo P2/P3. El parser distingue `fertiliz` / `bultos`.

### P5 — Aclaración

Si el ingest imprime `CLARIFICAR salida: Quimbaya`, el bot pregunta en
el grupo y espera un mensaje corto (`es el 3` / `El Alto`). Entonces
vuelve a parsear. Código de diálogo: pendiente; el contrato ya está.

### S1 — Plataforma y ESP32

Ya está: `prompts/01` desplegar, `02` sensor, `04` diagnosticar,
`05` tanque/hop. No son agentes de mensajería.

## Orden recomendado (después del chequeo / visita)

1. Pedido Amazon ×4 (cubetas, sin viento) — `docs/BOM.md`.
2. Excel de potreros → P1.
3. Un mensaje de prueba a mano (`--mensaje`) y mirar `/pastoreo`.
4. Recién entonces P2 (bot en el grupo).
5. Hermes/H1 cuando duela pegar el correo a mano.

## Qué no está listo (y no se finge)

- Bot de Telegram corriendo.
- Lectura automática de Gmail.
- OAuth Google / Mercado Pago.
- Excel crudo (.xlsx) sin pasar por CSV.
- Pronóstico oficial del tiempo.
