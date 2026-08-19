# Hermes — todavía no vive aquí

Hermes es el servicio que **lee** correo, PDFs y planillas y **escribe**
el resultado en ThingsBoard como si fuera un sensor más.

Este repositorio no lo implementa. El contrato, para cuando exista, es
el mismo HTTP que usa el ESP32:

```bash
# Attribute (fijo): source=hermes  —  lo pone add_sensor.py --source hermes
# Telemetría (por documento): no reutilices la clave "source" para el tipo de archivo.
curl -X POST "http://THINGSBOARD:8080/api/v1/$TOKEN/telemetry" \
  -H 'Content-Type: application/json' \
  -d '{"doc_type":"acopio_leche","litros":120,"precio":1800}'
```

Un Device por tipo de documento (o por sitio + tipo) basta.
ThingsBoard no distingue un DHT22 de un correo de planta.

Hasta que Hermes exista, no parsees correo dentro de este repo.
