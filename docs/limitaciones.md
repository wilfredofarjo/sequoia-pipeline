# Limitaciones y decisiones metodológicas

## Fechas internas de cámara

Los metadatos temporales originales no son confiables debido a reinicios del reloj de la cámara. Las fechas de adquisición reales se asignan desde bitácora de campo.

## GPS

Las imágenes auditadas no contienen coordenadas GPS XY utilizables. La reconstrucción se realiza en coordenadas locales.

## IMU

Yaw/Pitch/Roll están disponibles para la mayoría de las capturas, pero la relación absoluta con el frame SfM no se ha resuelto completamente.

Los resultados SfM–IMU se consideran diagnósticos y no se usan para forzar la alineación.

## Marcador CONT_C

`CONT_C` no corresponde a una esquina física exacta porque esa esquina no estaba completamente visible en las fotografías.

Las scale bars asociadas a CONT_C son referencias aproximadas y no deben interpretarse como errores métricos puros del modelo.

## Imágenes de calibración

Las 12 estaciones de panel permanecen en el proyecto para trazabilidad, pero están excluidas de la reconstrucción geométrica.

No todas las bandas presentan la misma facilidad de visualización. Los ajustes de brillo utilizados para dibujar máscaras modifican únicamente la visualización.

## Red Edge y NDRE

El canal Red edge mostró una relación radiométrica inesperada frente a NIR.

La prueba:

```text
B4 - B3
```

produjo valores mayoritariamente negativos en el ortomosaico, confirmando que el problema no se limita a la paleta de visualización.

Por tanto:

- NDRE queda fuera del análisis cuantitativo principal;
- no se invierte la fórmula;
- no se corrigen valores de forma ad hoc;
- el canal Red edge queda pendiente de una auditoría radiométrica específica.

## Índices recomendados actualmente

Índice principal:

- NDVI

Complementarios:

- GNDVI
- EVI2, después de normalizar reflectancia

## EVI estándar

El EVI estándar requiere una banda azul. Parrot Sequoia no dispone de banda azul en este conjunto de cuatro sensores, por lo que no se recomienda utilizar EVI clásico.

## Alcance de la validación

La reconstrucción SfM, la calibración radiométrica y los índices descritos se han validado inicialmente para la sesión 2026-08-21.

Las sesiones de mayo y julio deben reproducir el mismo pipeline antes de efectuar comparaciones temporales.

## Datos de gran tamaño

No se versionan en GitHub:

- TIFF originales;
- archivos DAT;
- proyectos PSX;
- nubes de puntos completas;
- depth maps;
- ortomosaicos completos.

El repositorio conserva código, parámetros, reportes ligeros y figuras de control.


## Dependencia de la bitácora para las fechas experimentales

Las fechas de sesión no se derivan de los metadatos temporales de los TIFF. Las tres fechas experimentales fueron tomadas de la bitácora de campo y utilizadas como referencia externa para particionar el dataset.

La información de nombres, carpetas, secuencias y fuente de almacenamiento se utiliza para asignar capturas a esas fechas, no para establecer fechas nuevas.

## Validación multi-sesión pendiente

La metodología completa se ha comprobado hasta ahora únicamente con la sesión 2026-08-21.

Las sesiones 2026-05-28 y 2026-07-10 están pendientes de:
- reconstrucción SfM completa;
- control de escala;
- calibración radiométrica;
- generación de ortomosaico;
- cálculo de índices;
- control de calidad radiométrico y geométrico.

Hasta completar esta réplica, no se asume equivalencia automática entre sesiones.

## Alcance de una futura etapa de ML

El uso de aprendizaje automático será una etapa posterior y no debe interpretarse como un componente ya validado del pipeline.

Antes de entrenar modelos se deberá definir:
- unidad de análisis;
- variables predictoras;
- variable objetivo;
- estrategia de partición de datos;
- prevención de fuga de información entre fechas o plantas;
- criterio de validación externa o temporal.

La consistencia de los índices entre sesiones es un requisito previo.
