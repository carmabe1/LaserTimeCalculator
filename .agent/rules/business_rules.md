---
trigger: always_on
---

# Business Rules - LaserTimeCalculator

## 1. Clasificación por Capas (Colores)
El sistema debe procesar el archivo SVG y clasificar las entidades según su atributo `stroke` o `fill`:

* **ROJO (#FF0000):** Proceso de **CORTE**. 
    * Lógica: Seguir el vector (Path).
    * Cálculo: `Tiempo = Distancia Total / Velocidad de Corte`.
* **VERDE (#00FF00):** Proceso de **MARCADO VECTORIAL** (Grabado en modo corte).
    * Lógica: Seguir el vector (Path).
    * Cálculo: `Tiempo = Distancia Total / Velocidad de Marcado`.
* **AZUL (#0000FF):** Proceso de **GRABADO RASTER**.
    * Lógica: Escaneo horizontal (X-axis) con avance vertical (Y-axis).
    * Cálculo: `Tiempo = ((Ancho del área / Velocidad) * (Alto del área / Paso)) + Tiempo de Overscan`.

## 2. Parámetros de Configuración Obligatorios
Para cada ejecución, el usuario debe proveer:
* `cut_speed` (mm/s)
* `vector_engrave_speed` (mm/s)
* `raster_engrave_speed` (mm/s)
* `scan_gap` (mm) -> Por defecto: 0.1mm.
* `transit_speed` (mm/s) -> Velocidad de movimiento con láser apagado.

## 3. Lógica de Estimación de Movimiento
* **Distancia Euclidiana:** Para movimientos de tránsito entre figuras, usar la distancia más corta entre el punto final de la entidad A y el inicial de la entidad B.
* **Tratamiento de Curvas:** Las curvas Bézier del SVG deben ser discretizadas en pequeños segmentos de línea para calcular su longitud total con precisión.
* **Ignorar Eje Z:** Cualquier referencia a profundidad o eje Z en el archivo o lógica debe ser ignorada.

## 4. Salida Esperada
El ejecutable debe retornar un JSON con:
* Tiempo total estimado (en segundos y formato HH:MM:SS).
* Desglose de tiempo por cada color/capa.
* Distancia total recorrida por el cabezal (quemando y en tránsito).