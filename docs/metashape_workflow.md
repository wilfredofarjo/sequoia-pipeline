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

## Align Photos

Configuración validada:

```yaml
accuracy: High
generic_preselection: true
reference_preselection: false
key_point_limit: 40000
tie_point_limit: 0
exclude_stationary_tie_points: true
guided_image_matching: false
adaptive_camera_model_fitting: true
```

`Reference preselection` se mantiene desactivado porque las imágenes auditadas no contienen coordenadas GPS XY válidas.

## Control de escala

El contenedor experimental tiene dimensiones nominales de:

- lado largo: 5.80 m
- lado corto: 2.25 m

Scale bars de control utilizadas:

```text
CONT_A–CONT_B = 2.25 m
CONT_A–CONT_D = 5.80 m
```

Scale bars asociados a `CONT_C` se consideran referencias geométricas aproximadas porque el punto físico exacto de la esquina no era visible en las imágenes.

La precisión de scale bars utilizada para la optimización fue:

```text
0.030 m
```

## Optimize Cameras

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

## Depth maps y point cloud

```yaml
depth_maps:
  quality: High
  filtering: Mild

point_cloud:
  points: 3148895
```

Se realizó ajuste conservador de la reconstruction region. La región se usa para limitar el volumen de trabajo; no se emplea como sustituto de una limpieza agresiva de puntos.

## Mesh

```yaml
source_data: Depth maps
surface_type: Arbitrary (3D)
quality: High
face_count: High
interpolation: Enabled
calculate_vertex_colors: true
reuse_depth_maps: true
```

Resultado inicial:

- faces: 340,429
- vertices: 171,904

El mesh se utiliza principalmente como soporte geométrico para ortorrectificación. El objetivo del proyecto no es maximizar detalle visual 3D.

## Orthomosaic

Configuración validada:

```yaml
type: Planar
projection_plane: Top XY
surface: Mesh
blending_mode: Mosaic
hole_filling: false
ghosting_filter: false
pixel_size_m: 0.00138395
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
