# Tenants, cooperativas y el plan de ~5 USD

ThingsBoard ya trae la jerarquía. No inventamos otra.

```
System admin
 └── Tenant          ← una cooperativa / un gremio / ANALAC / SAGAN
      ├── Users      ← técnicos de la cooperativa
      └── Customer   ← una finca
           └── Users ← el productor (solo ve sus dispositivos)
                └── Devices
```

## Cómo mapear el producto

| Idea de negocio | Objeto ThingsBoard |
|---|---|
| Plataforma (nosotros) | System admin |
| Cooperativa o gremio | **Tenant** |
| Finca que paga ~5 USD | **Customer** dentro de ese tenant |
| Productor | User del customer (permiso de solo lectura o de sus dispositivos) |
| Sensor | Device asignado a ese customer |

El productor entra a la misma UI, ve solo su finca, no la del vecino.

## Qué hacer en el PoC (hoy)

`scripts/bootstrap_finca.py` crea un **Customer** `Finca Demo` dentro del
tenant de demostración (`tenant@thingsboard.org`). Eso basta para:

- Harvey y un ESP32
- una finca piloto
- mostrar el aislamiento “yo veo lo mío”

## Cuando haya varias cooperativas

1. Entra como `sysadmin@thingsboard.org`.
2. *Tenants → Add tenant* (una por cooperativa).
3. Crea el tenant admin de esa cooperativa.
4. Ese admin crea un Customer por finca y le asigna dispositivos.

No hace falta otro microservicio. Si más adelante el gremio quiere marca
propia (logo, dominio, facturación), se evalúa ThingsBoard PE. No es el
paso 1.

## Precio de 5 USD

Eso es política comercial, no software. Técnicamente un customer + N
dispositivos no tiene costo de licencia en CE. El costo real es el
servidor (un VPS de 1–2 vCPU / 4 GB aguanta el PoC y varias fincas
chicas). El cobro al productor cubre hosting y soporte del gremio, no
una licencia por sensor.
