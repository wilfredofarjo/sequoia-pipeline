# Flujo SfM en Agisoft Metashape

## Objetivo

Reconstruir de forma independiente la geometría de una sesión Parrot Sequoia para disponer de una referencia SfM, escalar el modelo con dimensiones conocidas del contenedor y generar productos geométricos que soporten el análisis multiespectral.

## Sesión validada

El flujo descrito se validó inicialmente con la sesión **2026-08-21**.

- Capturas multiespectrales completas: 153
- Bandas por captura: Green, Red, Red edge, NIR
- Estaciones alineadas: 141 / 153
- Imágenes de calibración radiométrica: 12 estaciones, excluidas de la reconstrucción geométrica
- Tie points después de alineación: 107,798

## Importación

Metashape reconoce los TIFF individuales de Sequoia como un sistema multicámara.

La banda **Green** se utiliza como cámara master para la representación de cada estación. Esto no elimina ni sustituye las bandas Red, Red edge y NIR.

## Alineación de fotografías

Configuración validada:

```yaml
precision: Alta
preseleccion_generica: true
preseleccion_referencia: false
limite_puntos_clave: 40000
limite_puntos_enlace: 0
excluir_puntos_estacionarios: true
emparejamiento_guiado: false
ajuste_adaptativo_modelo_camara: true
```

`Reference preselection` se mantiene desactivado porque las imágenes auditadas no contienen coordenadas GPS XY válidas.

## Control de escala

De acuerdo con la bitácora experimental, la medición física del contenedor se realizó el **22 de mayo de 2026**. Estas mediciones se utilizaron posteriormente como referencia métrica para escalar el modelo SfM en Metashape mediante marcadores y barras de escala.

El contenedor experimental tiene dimensiones nominales de:

- lado largo: 5.80 m
- lado corto: 2.25 m

Scale bars de control utilizadas:

```text
CONT_A–CONT_B = 2.25 m
CONT_A–CONT_D = 5.80 m
```

Las scale bars asociadas a `CONT_C` se consideran referencias geométricas aproximadas porque el punto físico exacto de la esquina no era visible en las imágenes.

El procedimiento consistió en identificar en las imágenes puntos físicos correspondientes al contenedor, crear los marcadores `CONT_A`, `CONT_B`, `CONT_C` y `CONT_D`, proyectarlos en múltiples fotografías y construir barras de escala entre pares de marcadores. Las distancias medidas físicamente el 22 de mayo de 2026 se asignaron a las barras de control para transferir la escala real al modelo.

La precisión de las scale bars utilizada para la optimización fue:

```text
0.030 m
```

## Optimización de cámaras

Primera optimización:

- Fit f: ON
- Fit cx, cy: ON
- Fit k1: ON
- Fit k2: ON
- Fit k4: ON
- Fit p1: ON
- Fit p2: ON
- Fit k3: OFF
- Fit b1/b2: OFF

No se forzó la geometría para ajustar exactamente los checks asociados a `CONT_C`.

## Mapas de profundidad y nube de puntos

```yaml
mapas_profundidad:
  calidad: Alta
  filtrado: Suave

nube_puntos:
  puntos: 3148895
```

Se realizó un ajuste conservador de la región de reconstrucción. La región se usa para limitar el volumen de trabajo; no se emplea como sustituto de una limpieza agresiva de puntos.

## Malla

```yaml
datos_fuente: Mapas de profundidad
tipo_superficie: Arbitraria (3D)
calidad: Alta
numero_caras: Alto
interpolacion: Activada
calcular_colores_vertices: true
reutilizar_mapas_profundidad: true
```

Resultado inicial:

- faces: 340,429
- vertices: 171,904

La malla se utiliza principalmente como soporte geométrico para ortorrectificación. El objetivo del proyecto no es maximizar detalle visual 3D.

## Ortomosaico

Configuración validada:

```yaml
tipo: Planar
plano_proyeccion: Top XY
superficie: Mesh
modo_mezcla: Mosaic
relleno_huecos: false
filtro_ghosting: false
tamano_pixel_m: 0.00138395
```

Producto validado:

- tamaño: 2,648 × 4,552 px
- resolución: 1.38 mm/pixel
- sistema: Local Coordinates (m)
- bandas: 4, uint16

## Criterio de aceptación

La reconstrucción se considera suficientemente estable para análisis espectral cuando:

1. existe un único bloque geométrico coherente;
2. las plantas y el contenedor conservan continuidad espacial;
3. las scale bars principales mantienen errores compatibles con el montaje;
4. el ortomosaico conserva las cuatro bandas;
5. las imágenes de calibración permanecen fuera de la reconstrucción geométrica.


## Referencias relacionadas

- Agisoft LLC. (2025). *Agisoft Metashape User Manual — Professional Edition, Version 2.2*.
- Parrot. *Sequoia User Guide*.

Véase también [Referencias y documentos utilizados](referencias.md).
