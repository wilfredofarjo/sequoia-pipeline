# Índices de vegetación

## Orden de bandas del ortomosaico

```text
B1 = Green
B2 = Red
B3 = Red edge
B4 = NIR
```

## NDVI

```text
(B4-B2)/(B4+B2)
```

Se adopta como índice principal del flujo actual porque mostró una respuesta espacial coherente entre el dosel vegetal y las superficies no vegetales.

## GNDVI

```text
(B4-B1)/(B4+B1)
```

Se conserva como descriptor complementario sensible a la banda Green.

## EVI2

EVI2 no requiere banda azul y puede utilizarse como complemento cuando NDVI se acerca a saturación:

```text
2.5 * (NIR - Red) / (NIR + 2.4*Red + 1)
```

Debe calcularse sobre reflectancia normalizada a 0–1. Si el ortomosaico está almacenado como uint16 escalado, normalizar primero antes de aplicar el término constante +1.

## NDRE

```text
(B4-B3)/(B4+B3)
```

NDRE se evaluó, pero no se considera validado en la versión actual. La prueba directa `B4-B3` mostró valores mayoritariamente negativos, lo que indica una relación radiométrica NIR–Red edge que requiere auditoría específica.

## Exportación recomendada

- un GeoTIFF por índice y sesión;
- `Raster transform = Index value`;
- conservar NoData;
- compresión LZW;
- mantener resolución nativa cuando sea viable.

## Nomenclatura sugerida

```text
NDVI_2026-08-21.tif
GNDVI_2026-08-21.tif
EVI2_2026-08-21.tif
```
