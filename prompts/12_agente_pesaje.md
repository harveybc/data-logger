# Prompt — agente de producción por vaca (AM/PM)

---

En `data-logger` voy a cargar el pesaje/producción semanal. Lee
`docs/DATOS.md` (H3) y `ingest_plugins/pesaje_semanal.py`.

Columnas obligatorias: `fecha,placa,litros_am,litros_pm`.

1. Si te paso una tabla o una foto, arma un CSV con esas columnas
   (fecha ISO `YYYY-MM-DD`). No lo metas en git si tiene nombres reales.
2. `PYTHONPATH=. python3 -m app.ingest --pesaje /ruta/semana.csv`
3. Dime cuántas filas y el último día.

---
