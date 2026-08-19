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

UI: <http://127.0.0.1:5000> — menú Producción / Clima / Calidad (AdminLTE).

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
| **G1** | Pastoreo: polígonos, movimientos, fertilización, mapa | Hecho (CSV + parseo de mensaje; Excel cuando esté) |
| **L1** | Texto corto de “sin garantía / AS-IS” vs contrato del servicio | `docs/SERVICIO.md` |

## No hacer

- Volver al Flask AAA viejo (`docs/LEGACY.md`).
- Inventar login de ranchero en ThingsBoard. Dispositivos = token TB. Humanos del servicio = Google más adelante.
- ETL de sensores a un cubo propio. TB ya es la serie.
- Meter viento en el pedido de 4 juegos.
- Prometer pronóstico meteorológico oficial: solo tendencia de presión + lluvia medida.
