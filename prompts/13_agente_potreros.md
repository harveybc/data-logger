# Prompt — cargar potreros (Excel → CSV → mapa)

---

En `data-logger` voy a traer los polígonos del predio. Lee
`docs/PASTOREO.md` y `docs/AGENTES.md` (P1).

CSV: `sitio,numero,nombre,geojson`

1. Del Excel, una fila por potrero. `geojson` es un Polygon
   (lon,lat). No es GPS del ESP32.
2. No subas el Excel con datos personales a git si no lo pido.
3. `PYTHONPATH=. python3 -m app.ingest --potreros /ruta/potreros.csv`
4. Abre `/pastoreo` y confirma que se ven los polígonos.

Si el Excel usa WKT o columnas lat/lon sueltas, conviértelas a GeoJSON.
No inventes coordenadas.

---
