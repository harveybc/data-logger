# Pastoreo

Cuarto menú. Mapa de potreros + rotación + fertilización.

## Qué se guarda

| Tabla | Campos |
|---|---|
| `sitio` | nombre, usuario |
| `potrero` | sitio, **numero**, **nombre**, polígono GeoJSON |
| `pastoreo_mov` | potrero, fecha, momento (am/pm), tipo (entrada/salida), mensaje crudo |
| `fertilizacion` | potrero, fecha, abono, bultos, mensaje crudo |

Hover en un potrero: últimas 4–5 entradas/salidas y últimos abonos
(qué, cuándo, cuántos bultos). El que tiene el ganado ahora se pinta
verde (última **entrada** del sitio).

Los polígonos salen de Excel → CSV (`sitio,numero,nombre,geojson`).
No es GPS del sensor; es geometría del predio.

## Mensajes del operario (grupo / Telegram, después)

El agente parsea frases como:

- `17/08 tarde salieron del 3 y entraron al 5`
- `hoy en la mañana salieron de El Alto y entraron a La Vega`
- `17/08 fertilizamos el potrero 2 con urea 8 bultos`

Si no reconoce el nombre, responde `CLARIFICAR` (más adelante: pregunta
en el grupo). Hoy:

```bash
PYTHONPATH=. python3 -m app.ingest --potreros examples/fixtures/potreros.csv
PYTHONPATH=. python3 -m app.ingest --sitio "Sitio demo" \
  --mensaje "17/08 tarde salieron del 1 y entraron al 2"
```
