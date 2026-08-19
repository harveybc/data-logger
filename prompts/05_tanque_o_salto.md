# Prompt — tanque o nodo salto (no repetidor Wi‑Fi)

Copia el recuadro. No uses «granjero» ni «finca» al responderle al usuario;
sí «sitio», «tanque», «recinto», «customer».

---

En `data-logger` necesito cablear o flashear un sensor en un sitio con
radio dudosa. Lee `docs/HOP.md`, `docs/ENCIERRO.md` y `docs/DISENO.md` §3.

Reglas (no las reabras):

1. Un range extender / repetidor Wi‑Fi **no** es ingestión ni AAA.
2. Tanque metálico / CIP: electrónica **fuera** o **domo de techo** que
   escurre. Nivel = `firmware/esp32_tank_level_http` (JSN-SR04T,
   store-and-forward). Temperatura = DS18B20 en vaina, otro sketch.
   No boya. No hop dentro del metal.
3. Sombra RF **sin** Faraday: hijo `esp32_espnow_node` + padre
   `esp32_gateway_http`. Canal de AP fijo. Token del hijo solo en el padre.
4. Lo primero de campo sigue siendo el pluviómetro (`docs/PLUVIOMETRO.md`).

Dime qué sketch abrir, qué va en `secrets.h`, y el árbol de decisión
que aplicaste. No flashees si no hay placa en el escritorio.

---
