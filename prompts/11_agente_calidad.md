# Prompt — agente de calidad (PDF de liquidación)

---

En `data-logger` tengo un PDF de liquidación/calidad de la planta. Lee
`docs/DATOS.md`, `docs/AGENTES.md` (H2) e `ingest_plugins/planilla_calidad.py`.

1. No copies el PDF al repo (datos personales).
2. Corre `PYTHONPATH=. python3 -m app.ingest --planilla /ruta/al.pdf`.
   Si falta `pdftotext`, instálalo o usa pypdf; no reescribas el parser
   salvo que falle de verdad.
3. Reporta: periodo, proteína, grasa, sólidos, UFC, precio/L, días de
   litros leídos.
4. No inventes UFC. Si un campo sale `None`, dilo.

Luego puedo abrir http://127.0.0.1:5000/calidad.

---
