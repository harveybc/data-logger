# Recintos — hoja de taller

Primero el **prototipo de mesa**. El asistente de campo (huecos,
empaques, mangueras, conexiones a intemperie) entra cuando `rain_mm`
ya se ve en ThingsBoard.

Detalle: [DISENO.md](https://github.com/harveybc/data-logger/blob/master/docs/DISENO.md).
Pluviómetro: [PLUVIOMETRO.md](https://github.com/harveybc/data-logger/blob/master/docs/PLUVIOMETRO.md).
Compras: [BOM.md](https://github.com/harveybc/data-logger/blob/master/docs/BOM.md).

## 1A pluviómetro (primero) — una caja + toma

- IP66, plástico, ≥ 160 × 110 × 70 mm. Tapa 4 tornillos. No potear.
- PG9: pigtail 5 V mural → JST-XH. No USB de programación a la intemperie.
- PG7: cable de la electroválvula (fondo del cubo).
- ToF + BME280 secos bajo la tapa. Válvula en el punto más bajo.
- Lavado: manguera + jabón suave. Pasa de taller = **caja seca**.
- POST 200 = operador, no taller.

## Ambiente / hop (batería o mural)

- **Caja A** electrónica 120 × 80 × 55 mm. **Caja B** pack, aparte.
- Un JST a la platina: mural **XOR** pack. Nunca los dos (no es UPS).
- Platina v1: 4× M2.5. El rectángulo se congela en la primera platina;
  un FireBeetle futuro se atornilla a **esa** platina, no a huecos nuevos.
- GPIO 4 + 4.7 kΩ (DS18B20). Antena PCB: caja plástica, no metal.
- Pack = backup/demo ~10 h en DevKit despierto. Días/semanas **solo**
  placa de Iq bajo + `USE_DEEP_SLEEP` + `INTERVAL_S 3600`.
- `battery_v` no se mide en el rail 5 V.

## 1B tanque — clase CIP (no es la caja de jardín)

- CIP: ácido/álcali + desinfectante. El recinto de nivel es un **domo
  en el techo que escurre** (pendiente, sin charco sobre el transductor).
- Nada mecánico en la leche. Ensayo: JSN-SR04T. Radar 80 GHz después.
- Cable: puerto **existente** (boca de hombre, tri-clamp, CIP libre).
  No taladrar a ciegas.
- Temperatura = sonda en **vaina**, otro transductor, radio fuera.
- Electrónica fuera del metal, o en el domo si el domo es **plástico**.
