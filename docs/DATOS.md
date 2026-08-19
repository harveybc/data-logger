# De dónde sale cada número

Tres orígenes distintos. **No se mezclan en un cubo OLAP de sensores.**

| Origen | Ejemplo | Qué es | Dónde vive |
|---|---|---|---|
| Sensores (ESP32) | `rain_mm`, T, HR, presión, nivel de tanque | Serie continua | **ThingsBoard**. La UI la lee por API. No hay ETL. |
| Correo de acopio (planta) | Colácteos `noresponder@…`, ~1 día tarde | Un evento por día: litros, medida de tanque, ruta | **SQLite local** (`data/app.db`) vía plugin de ingestión |
| PDF de liquidación | Formato Colácteos quincenal | Calidad (proteína, grasa, sólidos, UFC), litros/día, precio | Misma SQLite |
| Planilla semanal del predio | Fecha, placa, litros AM, litros PM | Producción por animal y ordeño | Misma SQLite (CSV) |

## Campos que ya vimos (anónimos)

**Correo de recolección**

`fecha`, `codigo_productor`, `ruta`, `medida_tanque`, `litros`, `conductor`, `compartimiento`.

**PDF de liquidación / calidad**

- Cabecera: `precio_litro`, `periodo_desde`, `periodo_hasta`, `codigo_productor`.
- Litros por día del periodo.
- Composición (actual / última / penúltima / promedio): `proteina_pct`, `grasa_pct`, `solidos_pct`.
- Higiene: `ufc_x1000`, `frio_c` (a veces vacío).
- Sanidad: vigencias brucelosis / tuberculosis / BPG.
- Totales: `precio_final_litro`, `total_litros`, `total_pagar`.

**Pesaje / producción semanal por vaca**

`fecha`, `placa` (o nombre), `litros_am`, `litros_pm`.

## ¿ETL?

- **Sensores → plots de Clima / tanque:** no. ThingsBoard ya es la serie. AdminLTE consulta.
- **Documentos → Producción / Calidad:** sí, pero es **ingestión puntual** (parsear correo/PDF/CSV → tablas), no un star schema de experimentos.
- Más adelante, si un informe necesita “lluvia + litros del mismo día” en una sola SQL, un job chico **copia** agregados de TB a SQLite. Eso es opcional.

## Multiusuario (después)

Humanos en la web: **login con Google** (OAuth). Cada cuenta → un sitio (customer).  
Pagos web en Colombia: **Mercado Pago** (o Stripe), no “Google Payments” (eso es Play Store).  
Beta gratis: `plan=beta` en la cuenta; luego `plan=pago`.  
ThingsBoard sigue aislando la telemetría por tenant/customer.  
AAA de ranchero ≠ AAA de dispositivo (token ESP32).

No se implementa OAuth/pagos en el alpha de casa.

## Cómo cargar un documento

```bash
PYTHONPATH=. python3 -m app.ingest --email examples/fixtures/recoleccion_email.txt
PYTHONPATH=. python3 -m app.ingest --planilla /ruta/liquidacion.pdf
PYTHONPATH=. python3 -m app.ingest --pesaje examples/fixtures/pesaje_semanal.csv
```

Hermes, cuando exista, puede llamar al mismo parseo y escribir acá (o a TB si solo son litros).
