# Hermes — todavía no vive aquí

Hermes es el servicio que **lee** correo, PDFs y planillas y **escribe**
el resultado en ThingsBoard como si fuera un sensor más.

Este repositorio no lo implementa. El contrato, para cuando exista, es
el mismo HTTP que usa el ESP32:

```bash
curl -X POST "http://THINGSBOARD:8080/api/v1/$TOKEN/telemetry" \
  -H 'Content-Type: application/json' \
  -d '{"source":"email","doc_type":"acopio_leche","litros":120,"precio":1800}'
```

Un “dispositivo” por tipo de documento (o por finca + tipo) basta.
ThingsBoard no sabe ni le importa si el origen fue un DHT22 o un correo
de la planta.

Hasta que Hermes exista, no parsees correo dentro de este repo.
