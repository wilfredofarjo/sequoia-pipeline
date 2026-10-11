# Calibración radiométrica

## Objetivo

Convertir la respuesta de las imágenes multiespectrales Parrot Sequoia en un producto radiométricamente comparable entre bandas y adecuado para cálculo de índices de vegetación.

## Panel utilizado

Panel de reflectancia identificado como:

```text
Batch 4001
```

Valores impresos en el panel:

| Banda | Reflectancia |
|---|---:|
| Green | 0.189 |
| Red | 0.197 |
| Red edge | 0.221 |
| NIR | 0.255 |

Los valores se introducen como fracciones 0–1.

## Imágenes de calibración

En la sesión 2026-08-21 se identificaron 12 estaciones de calibración:

```text
CAP_000522 – CAP_000533
```

Estas estaciones permanecen deshabilitadas para la reconstrucción geométrica.

## Detección del panel

`Locate Panels` reconoció el identificador del panel, pero la asociación automática no fue suficiente para todas las bandas.

Se utilizó una ruta manual:

1. abrir cada banda de una captura de calibración;
2. ajustar brillo únicamente para visualización cuando fue necesario;
3. seleccionar el rectángulo gris de referencia;
4. crear una máscara;
5. invertir la máscara para dejar libre únicamente el área gris;
6. repetir por banda cuando la señal permitía identificar el panel.

Las máscaras afectan la selección radiométrica, no modifican los TIFF originales.

## Calibración de reflectancia

Configuración:

```text
Use reflectance panels = ON
Use sun sensor         = OFF
```

Los valores del panel se introdujeron manualmente.

## Normalización de sensibilidad entre bandas

Se confirmó `Normalize band sensitivity` activado para las cuatro cámaras.

Parámetros observados en Camera Calibration:

| Banda | Black level | Sensitivity |
|---|---:|---:|
| Green | 3252.18 | 484.109 |
| Red | 4791.92 | 443.518 |
| Red edge | 5004.66 | 133.927 |
| NIR | 4854.96 | 490.047 |

Estos parámetros no se modifican manualmente.

## Producto

El ortomosaico resultante conserva:

```text
B1 = Green
B2 = Red
B3 = Red edge
B4 = NIR
```

Tipo:

```text
4 bandas, uint16
```

## Índices

### NDVI

```text
(B4-B2)/(B4+B2)
```

El NDVI presentó una respuesta espacial coherente entre vegetación y estructuras no vegetales y se adopta como índice principal del flujo actual.

### GNDVI

```text
(B4-B1)/(B4+B1)
```

Disponible como descriptor complementario.

### NDRE

```text
(B4-B3)/(B4+B3)
```

Durante la validación se observó que gran parte del dosel presenta `NIR < Red edge`, generando NDRE predominantemente negativo. Por esta razón NDRE no se considera validado para análisis cuantitativo en la versión actual.

### EVI2

EVI2 puede utilizarse como alternativa que no requiere Red edge ni banda azul:

```text
2.5 * (NIR - Red) / (NIR + 2.4*Red + 1)
```

El término constante `+1` requiere que NIR y Red estén expresados en reflectancia 0–1. No debe aplicarse directamente sobre valores uint16 escalados sin normalización previa.

## Exportación

Para exportar un índice desde Metashape:

- formato: GeoTIFF;
- `Raster transform = Index value`;
- conservar NoData;
- compresión LZW;
- mantener la resolución nativa cuando sea viable.

Para trazabilidad, se recomienda un archivo por índice y sesión.
