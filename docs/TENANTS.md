# Tenants y sitios

ThingsBoard ya trae la jerarquía. No inventamos otra.

```
System admin
 └── Tenant          ← quien opera la plataforma (un gremio, una empresa)
      ├── Users      ← técnicos
      └── Customer   ← un sitio / un cliente
           └── Users ← solo ven los dispositivos de ese sitio
                └── Devices
```

| Idea de producto | Objeto ThingsBoard |
|---|---|
| Quien hospeda | System admin |
| Organización | **Tenant** |
| Sitio o cliente | **Customer** |
| Usuario final | User de ese customer |
| Sensor | Device asignado al customer |

## PoC de hoy

`scripts/bootstrap_finca.py` crea un Customer de demostración en el
tenant `tenant@thingsboard.org`. Basta para un ESP32 y para mostrar
“yo veo lo mío”.

## Varios clientes

1. Entra como `sysadmin@thingsboard.org`.
2. *Tenants → Add tenant* si cada organización debe ir aislada.
3. Ese admin crea un Customer por sitio y le asigna dispositivos.

Marca propia (logo, dominio, facturación) es ThingsBoard PE. No es el
paso 1.

El cobro por sitio (si algún día hay servicio) es política comercial.
CE no cobra licencia por sensor; el costo es el servidor.
