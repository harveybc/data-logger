# Plan de trabajo — aplicación de telemetría

Software y diseños de hardware: **abiertos** (MIT). El cobro, si lo hay,
es por **hospedar y soportar**, no por una licencia por sensor.

ThingsBoard CE sigue siendo el almacén. Este repo es el puente, el
firmware y (ahora) un **pipeline de plugins** + una **interfaz web**
de ejemplo.

## Señal de clima: presión, no viento

En campo, “se nubló y paró el viento → llueve” / “empezó a ventear →
no llueve” se parece a un frente y a un cambio de presión. Un **BME280**
(ya en el pedido ×4) mide presión sin partes móviles.

El viento (cubeta + anemómetro + veleta) queda como **extra de pago /
versión premium**: más caro, más mantenimiento. No va en el lote alpha.

## Arquitectura (igual que el resto de la casa)

1. JSON global (`examples/config/leche_default.json`).
2. Cada plugin declara `plugin_params`; si el JSON trae la misma clave,
   gana el JSON. `plugins.web` y `plugins.pipeline` se aplanan encima.
3. Flags `--largos` ganan al archivo.
4. El **pipeline** carga los demás plugins y los corre.
5. Hoy: `pipeline=default` → `web=adminlte`.
   Mañana: el mismo pipeline puede cargar Hermes, alertas, etc.

```
PYTHONPATH=. python3 -m app.main --load_config examples/config/leche_default.json
```

UI: <http://127.0.0.1:5000> — Producción / Clima / Calidad / Pastoreo.

## Agentes (crearlos, no fingir que ya corren)

Instrucciones completas: **[docs/AGENTES.md](AGENTES.md)**.
Prompts de copiar y pegar: `prompts/10`–`16`.

| Cuándo | Prompt |
|---|---|
| Correo de acopio | `prompts/10_agente_acopio.md` |
| PDF de calidad | `prompts/11_agente_calidad.md` |
| Pesaje AM/PM | `prompts/12_agente_pesaje.md` |
| Excel de potreros | `prompts/13_agente_potreros.md` |
| Escribir el bot Telegram | `prompts/14_crear_bot_telegram.md` |
| Alma 24/7 del grupo | `prompts/15_alma_pastoreo.md` |
| Un mensaje de rotación hoy, a mano | `prompts/16_agente_rotacion_manual.md` |

Parsers y puentes **están**. Lo que falta es **tuyos**: buzón IMAP,
token Telegram, Excel, foto de pesaje. Lista: [docs/ACCIONES.md](ACCIONES.md).

## Entregas

| ID | Qué | Estado |
|---|---|---|
| **A0** | Compose ThingsBoard + scripts + firmware cubeta/DHT/tanque/hop | Hecho |
| **A1** | Loader + merger + pipeline + plugin web AdminLTE (3 menús) | Hecho (este cambio) |
| **A2** | Clima real: `rain_mm` + T/HR + **presión** y texto de tendencia | Hecho (lee TB; vacío si no hay datos) |
| **B1** | Correo de acopio → SQLite → Producción | Hecho (`app.ingest --email`, campos Colácteos) |
| **B2** | Tanque de frío en Producción (`device_tanque`) | Firmware listo; lee TB, no SQLite |
| **B3** | Producción por vaca AM/PM (`fecha,placa,litros_am,litros_pm`) | Hecho (`--pesaje` CSV) |
| **C1** | PDF liquidación: proteína, grasa, sólidos, UFC, precio | Hecho (`--planilla`); alertas UFC |
| **P1** | Anemómetro / veleta como extra | No en alpha |
| **S1** | Login Google + plan beta/pago + Mercado Pago | Después; `docs/SAAS.md` |
| **R1** | Roles admin / veterinario / operario + varios sitios | Hecho (`?rol=`, `docs/ROLES.md`) |
| **G1** | Pastoreo: polígonos, movimientos, fertilización, mapa | Hecho (CSV + parseo; Excel y bot Telegram pendientes) |
| **G2** | Cómo crear cada agente (H1–H3, P1–P5, S1) | Hecho: `docs/AGENTES.md` + `prompts/10`–`16` |
| **G3** | Puente Telegram (`python3 -m app.telegram_pastoreo`) | Hecho; falta tu token en `.env` |
| **H0** | IMAP acopio: desde última fecha, varios mails, borrar solo si OK | Hecho (`--imap`); falta el buzón nuevo |
| **H4** | Excel potreros (`--potreros-xlsx`) | Hecho; falta el archivo |
| **H5** | OCR pesaje lunes/martes | Hecho (`--ocr-pesaje`); falta tesseract + foto |
| **L1** | Texto corto de “sin garantía / AS-IS” vs contrato del servicio | `docs/SERVICIO.md` |

## No hacer

- Volver al Flask AAA viejo (`docs/LEGACY.md`).
- Inventar login de ranchero en ThingsBoard. Dispositivos = token TB. Humanos del servicio = Google más adelante.
- ETL de sensores a un cubo propio. TB ya es la serie.
- Meter viento en el pedido de 4 juegos.
- Prometer pronóstico meteorológico oficial: solo tendencia de presión + lluvia medida.
