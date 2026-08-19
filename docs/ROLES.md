# Roles (humanos)

No confundir con el token del ESP32.

| Rol | Ve | No ve / no hace |
|---|---|---|
| **admin** | Todo, todos los sitios, accounting, authorization, usuarios | — |
| **veterinario** | Producción, clima, calidad, pastoreo de *sus* sitios | Otros usuarios, accounting, configurar authorization |
| **operario** | Solo lectura: producción, clima, pastoreo | Calidad; no escribe configuración |

Un usuario puede tener **varios sitios** (predios / conjuntos de sensores).
Sin GPS en los nodos. El sitio se elige en la barra superior.

Hoy el rol se simula con `?rol=admin|veterinario|operario` o
`current_role` en el JSON. Google Sign-In viene después (`docs/SAAS.md`).
