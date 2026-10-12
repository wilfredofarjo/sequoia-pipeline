# Diseño experimental y unidad de análisis

## Material vegetal

El experimento se desarrolló con plantas de piña (*Ananas comosus*), cultivar MD2.

Las plantas fueron sembradas el **16 de octubre de 2025**, utilizando material de siembra tipo **hijo basal**, con un peso inicial aproximado de **300 g por planta**.

El ingreso de las plantas al ambiente controlado se realizó el **14 de mayo de 2026**, correspondiente a **210 días después de la siembra**.

## Población experimental

El contenedor experimental incluyó un total de **30 plantas**, distribuidas espacialmente en una matriz de:

```text
2 columnas × 15 filas longitudinales
```

La unidad principal de análisis definida para la etapa actual del proyecto es el **dosel conjunto de las 30 plantas**.

Aunque se dispone de información individual de peso y posición, en esta fase no se considera cada planta como una unidad experimental independiente para el análisis espectral principal.

## Referencia espacial dentro del contenedor

La distribución de plantas posee una referencia espacial asociada a los marcadores físicos utilizados posteriormente para escalar la reconstrucción SfM.

Dos posiciones permiten orientar el arreglo dentro del sistema local:

```text
Planta 1  → esquina CONT_D
Planta 29 → sector correspondiente a CONT_B
```

Estas referencias permiten relacionar la matriz biológica 2 × 15 con la geometría reconstruida del contenedor.

La numeración de plantas debe conservarse durante las etapas posteriores de segmentación espacial para mantener trazabilidad entre posición física, peso de planta, imágenes, ortomosaico e índices espectrales.

## Distribución espacial del peso de las plantas

Se dispone de un registro de peso individual asociado a la ubicación de cada planta dentro del contenedor.

| Fila longitudinal | Columna 1 (lb) | Columna 2 (lb) |
|---|---:|---:|
| 15 | 8.9 | 7.6 |
| 14 | 12.8 | 5.5 |
| 13 | 5.1 | 1.4 |
| 12 | 5.9 | 7.1 |
| 11 | 10.0 | 10.0 |
| 10 | 7.0 | 9.5 |
| 9 | 5.0 | 5.2 |
| 8 | 6.1 | 2.9 |
| 7 | 7.0 | 6.3 |
| 6 | 7.4 | 5.6 |
| 5 | 9.4 | 7.9 |
| 4 | 2.3 | 9.4 |
| 3 | 14.9 | 4.3 |
| 2 | 11.8 | 8.1 |
| 1 | 7.4 | 10.4 |

Esta variabilidad de peso constituye una fuente potencial de heterogeneidad estructural y fisiológica dentro del dosel.

## Decisión sobre segmentación

Desde una perspectiva metodológica, una alternativa futura sería segmentar espacialmente el dosel considerando posición de cada planta, peso individual, agrupaciones por rango de peso y respuesta espectral local.

Sin embargo, para la etapa actual se adopta un enfoque más conservador y reproducible:

> El dosel completo de las 30 plantas se considera una única unidad de análisis espacial.

La información individual se conserva para una futura fase de segmentación o análisis de subzonas.

## Cronología de adquisición

Las sesiones de imágenes fueron definidas a partir de la bitácora de campo.

| Evento | Fecha | Edad desde siembra |
|---|---|---:|
| Siembra | 2025-10-16 | 0 días |
| Ingreso a ambiente controlado | 2026-05-14 | 210 días |
| Sesión fotográfica 1 | 2026-05-28 | 224 días |
| Sesión fotográfica 2 | 2026-07-10 | 267 días |
| Sesión fotográfica 3 | 2026-08-21 | 309 días |

Las sesiones fotográficas corresponden aproximadamente a 14, 57 y 99 días después del ingreso a ambiente controlado, respectivamente.

## Factor lumínico y sistema de iluminación

El ambiente controlado utilizó lámparas **Spider Farmer SF-G4500** como fuente artificial de iluminación del dosel.

La configuración experimental documentada incluye dos luminarias con eficiencia nominal de **2.8 µmol J⁻¹**, operadas al **60 % de potencia**. La altura aproximada del dosel fue de 1.10–1.25 m y la separación lámpara-dosel utilizada como referencia operacional fue cercana a 0.74 m. El objetivo lumínico del sistema fue un DLI aproximado de **18 mol m⁻² d⁻¹**.

La intensidad de operación de las lámparas se mantuvo estable durante cada periodo de encendido. El factor experimental que varió fue la **duración diaria de exposición a la luz**, es decir, el fotoperiodo.

Las plantas fueron sometidas a una **simulación del horario semanal de luz correspondiente al periodo comprendido entre las semanas 47 y 9**, con base en el cronograma previamente calculado para reproducir la variación estacional de horas luz.

Los valores exactos de duración de luz por semana deben conservarse como parte del registro experimental y añadirse al repositorio una vez se consolide la tabla definitiva de la bitácora.

### Caracterización fotónica pendiente

Se realizó una medición con equipo para cuantificar la radiación fotosintéticamente activa a nivel del dosel. La variable relevante para documentar esta medición es **PPFD** (*Photosynthetic Photon Flux Density*), expresada en:

```text
µmol m⁻² s⁻¹
```

La incorporación de estos datos al repositorio se encuentra pendiente.

Debe distinguirse entre:

- **PPF**: flujo fotónico fotosintético total emitido por una fuente, en µmol s⁻¹;
- **PPFD**: densidad de flujo fotónico que alcanza una superficie, en µmol m⁻² s⁻¹.

Para este experimento, la variable de mayor interés para caracterizar la luz recibida por las plantas es PPFD.

## Unidad de análisis espectral

La unidad principal de análisis será el dosel total.

Para cada sesión se propone obtener variables resumen de la distribución espectral del dosel, incluyendo media, mediana, desviación estándar, coeficiente de variación y percentiles 10, 50 y 90.

Las variables espectrales candidatas son:

- reflectancia NIR;
- NDVI;
- GNDVI;
- EVI2, una vez estandarizado su cálculo.

NDRE permanece temporalmente excluido del análisis principal hasta completar la validación radiométrica del canal Red Edge.
