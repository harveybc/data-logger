# Lista de compras — prototipo primero

Este repo **no** está dentro de `predictor`. En el computador:

`/home/harveybc/Documents/GitHub/data-logger`

En GitHub: <https://github.com/harveybc/data-logger>

Precios de Mercado Libre Colombia y Amazon, agosto 2026. Van a
moverse; los enlaces son de búsqueda / ficha. **No hace falta comprar
todo si ya tienes ESP32, sensores y electroválvula:** primero prueba
en protoboard lo que hay en el cajón.

El **asistente de campo** entra después: huecos, empaques, mangueras y
conexiones eléctricas para que resista el ambiente. No elige sensores.

## Orden

1. **Pedido Amazon (recomendado):** pluviómetro comercial de **cubeta
   basculante** (pulse/reed). El ESP32 que ya tienes cuenta vuelcos y
   manda `rain_mm` a ThingsBoard. No hace falta cubo, ToF ni válvula.
2. Mesa: ESP32 + el instrumento + 2 hilos. Sketch
   `firmware/esp32_tipping_bucket_http/`.
3. Montaje de intemperie (asistente de campo) cuando `rain_mm` se vea
   en la UI.

El cubo+válvula queda como plan B si ya tienes esas piezas y no quieres
esperar un envío.

---

## Pluviómetro comercial (lo que sí conviene pedir en Amazon)

Ninguna estación “con app” (BALDR, Netatmo, Ambient de consumo) habla
ThingsBoard. Lo que sí existe y **guarda los datos como diseñamos**
(`rain_mm` en TB, acumulado del día, reset a medianoche) es un
**instrumento meteorológico de cubeta** + nuestro ESP32.

| Qué pedir | Por qué | Enlace | ≈ |
|---|---|---|---|
| **Cubeta basculante con salida de pulso** (reed). 1 vuelco ≈ 0.2 mm o 0.279 mm. Se vacía sola. | Estándar de pastos / meteo. 2 hilos a GPIO + GND. | [Amazon: tipping bucket rain gauge Arduino](https://www.amazon.com/s?k=tipping+bucket+rain+gauge+arduino) · [DFRobot SEN0575](https://www.dfrobot.com/product-2689.html) (~US$30, I2C/UART) | US$20–40 el sensor solo |
| **SparkFun Weather Meter Kit** (SEN-08942) | Misma cubeta + anemómetro y veleta (viento lo querías después). | [Amazon B084DBXMPX](https://www.amazon.com/dp/B084DBXMPX) · [SparkFun](https://www.sparkfun.com/weather-meter-kit.html) | US$80–100 el kit |
| **Davis 6466 / 6463 Rain Collector** | El de estaciones profesionales. Reed 0.2 mm. | [Amazon: Davis rain collector](https://www.amazon.com/s?k=Davis+6466+rain+collector) | US$80–150 |
| Hydreon **RG-15** (óptico, sin partes móviles) | Menos atascos; ±10 %; UART o emula cubeta. Reviews mixtos vs Davis en mm. | [ficha oficial](https://rainsensors.com/products/rg-15/) ~US$99 | Solo si odias limpiar hojas |

**No pidas** para este uso: pluviómetros “smart” solo-app, Ecowitt WH40
*sin* plan de adaptador (el gateway Ecowitt puede subir a un HTTP
propio, **no** al Device API de ThingsBoard sin un script extra).

Firmware: `esp32_tipping_bucket_http`. En `secrets.h`:
`TIP_PIN 27`, `MM_PER_TIP 0.2` (o `0.2794` si es SparkFun: 0.011").

---

## Plan B — cubo + válvula (si no compras cubeta)

El cubo está enchufado: no pagues sensor de µA. Prioridad: barato,
fácil de conseguir en Colombia, que el firmware ya soporta.

| Pieza | Para qué | Mercado Libre CO | Amazon | ≈ |
|---|---|---|---|---|
| **Ya lo tienes** | ESP32, sensores, electroválvula | — | — | $0 |
| Cubo / botella de área conocida + embudo | Acumular lluvia | Ferretería / cualquier taza plástica | — | $0–15 mil |
| **IRLZ44N o módulo IRF520** + **1N4007** | MOSFET + flyback para la válvula 12 V (el ESP32 no mueve la bobina solo) | [IRF520](https://listado.mercadolibre.com.co/modulo-irf520) · [1N4007](https://listado.mercadolibre.com.co/1n4007) | [IRLZ44N](https://www.amazon.com/s?k=IRLZ44N) | 5–15 mil / US$1–4 |
| Fuente 12 V ≥ 1 A (si la válvula es 12 V) | Solo la bobina. El ESP32 sigue en 5 V USB | [fuente 12V 1A](https://listado.mercadolibre.com.co/fuente-12v-1a) | [12V 1A adapter](https://www.amazon.com/s?k=12V+1A+power+adapter) | 15–30 mil |
| Protoboard + jumpers | Prototipo de mesa | [protoboard](https://listado.mercadolibre.com.co/protoboard-65) | — | 10–20 mil |

### Sensor de nivel del cubo (elige **uno**; el más barato que ya tengas gana)

| Opción | Cuándo | Enlace | Notas |
|---|---|---|---|
| **El que ya tienes** | Primera prueba | — | Si es ultrasónico JSN, el cubo debe ser **> 25 cm** de alto (zona ciega). Si es ToF láser, tapa seca. Si es sonda analógica de nivel, óxido a medio plazo: solo prototipo. |
| ToF **VL53L1X** | Cubo chico (< 20 cm), tapa seca | ML: [módulo VL53L1X](https://listado.mercadolibre.com.co/vl53l1x) (~35–45 mil, p.ej. [Dweii](https://www.mercadolibre.com.co/dweii-vl53l1x-sensor-distancia-tof-1575in/p/MCO2051785266)) · Amazon: [VL53L1X](https://www.amazon.com/s?k=VL53L1X+ESP32) (~US$8–12) | Es el default del sketch `esp32_pluviometro_http`. |
| Sonda analógica de nivel | Lo más barato si no hay ToF | [sensor nivel agua Arduino](https://listado.mercadolibre.com.co/sensor-nivel-agua-arduino) | No para intemperie larga. |
| **No** JSN-SR04T en cubo de vaso | Zona ciega ~20–25 cm | — | Sí sirve en tanque alto. |

### Clima extra (opcional; el pluviómetro funciona sin esto)

| Pieza | ML | Amazon | ≈ |
|---|---|---|---|
| **BME280** (T + HR + presión) — un chip | [BME280](https://listado.mercadolibre.com.co/bme280) · ficha [Mactrónica](https://www.mactronica.com.co/sensor-de-presion-y-humedad-bme280) / [artículo ML](https://articulo.mercadolibre.com.co/MCO-1333437915-sensor-de-presion-temperatura-y-humedad-bme280-_JM) | [BME280](https://www.amazon.com/s?k=BME280+sensor) ~US$8–13 | 15–25 mil |
| **DHT22** si no hay BME280 | [DHT22](https://listado.mercadolibre.com.co/dht22) | [DHT22](https://www.amazon.com/s?k=DHT22+AM2302) | 10–15 mil |
| BMP280 (presión + temp, **sin** humedad) | más barato, peor para pastos | evitar si quieres HR | — |

Viento: no comprar ahora.

### Electroválvula

Si la que tienes es **12 V NC (normalmente cerrada)** de 1/4" o 1/2" para
agua, úsala. Si hay que comprar:

- ML: [válvula solenoide 12 V](https://listado.mercadolibre.com.co/valvula-solenoide-12v) — unidades ~25–40 mil; [kit 2× 1/2"](https://www.mercadolibre.com.co/kit-2-electrovalvula-12v-12-agua-automatizacion-vzds23/p/MCO2085914209) ~45–56 mil.
- Amazon: [DIGITEN 12 V 1/4"](https://www.amazon.com/DIGITEN-Solenoid-Connect-normally-Closed/dp/B016MP1HX0) ~US$10.

Hace falta **presión casi cero** al vaciar un cubo: las válvulas de
lavadora a veces no abren sin red de agua. Si la tuya no drena el cubo
en mesa, busca “solenoide 12 V **sin presión** / gravity feed”.

---

## Tanque (bajo consumo; **después** del pluviómetro)

Electrónica **fuera** del metal o en un domo plástico. El sensor mira
hacia abajo. No boya.

| Pieza | Consumo | Por qué | Dónde |
|---|---|---|---|
| **A02YYUW** (UART, IP67) | ~5 mA reposo, ~8 mA midiendo; ciega 3 cm | Mejor para batería + CIP splash. 3.3–5 V. | Amazon: [A02YYUW](https://www.amazon.com/s?k=A02YYUW+waterproof+ultrasonic) ~US$15–22. ML: buscar `A02YYUW` / `sensor ultrasonico UART impermeable`. |
| **JSN-SR04T / AJ-SR04M** | ~30 mA midiendo, ciega **20–25 cm** | Más barato; OK si hay toma y el tanque es alto. Default del sketch actual. | Amazon: [JSN-SR04T](https://www.amazon.com/Waterproof-Ultrasonic-JSN-SR04T-Integrated-Transducer/dp/B07FQCNXPP) ~US$8–12. ML: [jsn-sr04t](https://listado.mercadolibre.com.co/jsn-sr04t). |
| Radar 80 GHz de proceso | bajo, aguanta vapor/espuma | Caro; no es el prototipo. | Industrial (VEGA / Endress), no ML de hobby. |

Para **muy bajo consumo** no cambies de familia a ciegas: un ESP32 en
`deep sleep` + un ping de 100 ms cada 15 min gasta casi nada aunque el
sensor tome 8–30 mA *mientras mide*. El A02YYUW gana porque duerme a
~5 mA y no tiene 25 cm ciegos (útil si el tanque se llena hasta el techo).

---

## Qué no comprar todavía

- Caja IP66, prensaestopas, platina: eso es el montaje de campo **después**
  de que el protoboard publique `rain_mm`.
- Anemómetro.
- ThingsBoard PE, LoRa, radar industrial.

## Cómo saber si “lo que tienes sirve”

| Lo que hay en el cajón | ¿Sirve de proto? |
|---|---|
| ESP32 DevKit + USB | Sí. Mesa / mural. No promete semanas a pila. |
| Electroválvula 12 V + MOSFET + diodo | Sí, si abre **sin** presión de red. |
| DHT22 / BME280 | Sí, opcional en el pluviómetro. |
| HC-SR04 (el azul de protoboard) | Mesa seca. No intemperie ni CIP. |
| JSN-SR04T | Tanque alto o cubo **alto**. No vaso chico. |
| VL53L1X / VL53L0X | Cubo chico, tapa seca. VL53L0X llega ~1–2 m, igual sirve en un cubo. |
