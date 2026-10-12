# Índices de vegetación

## Orden de bandas del ortomosaico

```text
B1 = Green
B2 = Red
B3 = Red edge
B4 = NIR
```

## Fundamento bibliográfico de la selección

La selección de variables espectrales e índices del proyecto se apoya en revisiones recientes sobre fisiología vegetal, estrés y comportamiento de índices multiespectrales.

Pérez-Chimal et al. (2026) reportan que **NDVI** fue el índice más frecuente en la literatura revisada, presente en aproximadamente el 87 % de los estudios, principalmente para estimar vigor, biomasa y estructura del dosel. La misma revisión identifica **NDRE** y **GNDVI** entre los índices empleados para clorofila y detección de estrés, y señala que las bandas **Red Edge** y **NIR** son especialmente relevantes para vigor, clorofila y respuestas fisiológicas. También destaca que la calibración radiométrica, la estabilidad de la iluminación y la validación metodológica son determinantes para interpretar correctamente los índices (Pérez-Chimal et al., 2026).

Haque et al. (2024) describen NDVI, NDRE, GNDVI y EVI entre los índices comunes derivados de imágenes multiespectrales. La revisión advierte que **NDVI puede saturarse en doseles densos**, por lo que conviene complementarlo con otros índices. También enfatiza que condiciones ambientales, iluminación y calibración pueden modificar la reflectancia y la respuesta de los índices, lo que respalda el uso de un flujo radiométrico estandarizado entre sesiones.

Zandi et al. (2025) vinculan la reflectancia en **NIR** y Red Edge con cambios fisiológicos asociados al estrés vegetal. La revisión señala que respuestas de estrés hídrico pueden acompañarse de cambios en la reflectancia NIR y que síntomas como enrollamiento foliar, marchitez o alteraciones estructurales pueden formar parte de la respuesta al estrés. En este proyecto, esta evidencia respalda tratar la señal NIR como una **variable espectral de interés**, pero no como un diagnóstico causal por sí sola.

Con base en esta bibliografía y en el comportamiento observado en la sesión 2026-08-21, la selección actual se interpreta así:

| Variable / índice | Fundamentación bibliográfica | Estado en el proyecto |
|---|---|---|
| **NIR** | Sensible a estructura foliar y cambios asociados al estado fisiológico y estrés | Variable espectral principal de interés |
| **NDVI** | Índice ampliamente utilizado para vigor, biomasa y estructura del dosel | Índice principal |
| **GNDVI** | Complementa NDVI utilizando Green + NIR; útil para variación de vigor y clorofila | Índice complementario |
| **EVI2** | La familia EVI ayuda a complementar NDVI cuando existe saturación; EVI2 se adopta por no requerir banda azul | Pendiente de estandarización |
| **NDRE** | La literatura respalda su utilidad para clorofila y estrés | **En revisión radiométrica** por el comportamiento anómalo del canal Red Edge observado en este dataset |

La bibliografía, por tanto, **respalda la selección conceptual de NDVI, GNDVI, EVI/EVI2, NDRE y NIR**, mientras que el control de calidad del propio dataset determina cuáles pueden utilizarse finalmente en el análisis cuantitativo. La exclusión temporal de NDRE no contradice su utilidad reportada en la literatura; responde a una inconsistencia radiométrica específica que debe resolverse antes de incorporarlo.


## NDVI

```text
(B4-B2)/(B4+B2)
```

Se adopta como índice principal del flujo actual porque mostró una respuesta espacial coherente entre el dosel vegetal y las superficies no vegetales. Esta elección coincide con su uso extensivo en la literatura para vigor, biomasa y estructura del dosel, aunque debe considerarse su posible saturación en coberturas densas.

## GNDVI

```text
(B4-B1)/(B4+B1)
```

Se conserva como descriptor complementario sensible a la banda Green y como apoyo a la interpretación de variaciones de vigor y clorofila.

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

NDRE se evaluó porque la literatura lo reconoce como un índice relevante para clorofila y estrés. Sin embargo, no se considera validado en la versión actual: la prueba directa `B4-B3` mostró valores mayoritariamente negativos, lo que indica una relación radiométrica NIR–Red edge que requiere auditoría específica.

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


## Referencias relacionadas

- Pérez-Chimal et al. (2026) — revisión sistemática sobre índices, firmas espectrales y rasgos fisiológicos vegetales.
- Zandi et al. (2025) — revisión de análisis multimodal para evaluación de estrés vegetal y respuesta espectral.
- Haque et al. (2024) — revisión sobre efectos ambientales, calibración y comportamiento de índices multiespectrales.
- Gitelson, Kaufman & Merzlyak (1996) — uso del canal verde en índices de vegetación.
- Jiang, Huete, Didan & Miura (2008) — EVI2 sin banda azul.

Véase también [Referencias y documentos utilizados](referencias.md).
