# Workflow

## 1. Adquisición

Cada disparo Parrot Sequoia puede producir:

- GRE — Green
- RED — Red
- REG — Red Edge
- NIR — Near Infrared
- RGB — imagen RGB de referencia

Para WebODM, el conjunto multiespectral se procesa con GRE + RED + REG + NIR.

## 2. Inventario

El pipeline recorre recursivamente `Interna/` y `SD/`.

Se excluyen:

- `.thumb`
- `Zip_Originales`
- `__MACOSX`
- carpetas de salida del propio pipeline

## 3. Validación de capturas

Una captura multiespectral se considera completa si contiene:

```text
GRE + RED + REG + NIR
```

El RGB no es requisito para considerar completa una captura.

## 4. Duplicados

Se usa SHA-256 para identificar archivos idénticos sin depender de fechas o nombres.

## 5. Reconstrucción de sesiones

Debido a reinicios del reloj de la cámara, la fecha embebida no se trata como verdad experimental.

Las **fechas utilizadas para particionar el conjunto de imágenes en sesiones experimentales corresponden a fechas registradas en la bitácora de campo**. No fueron inferidas a partir de los metadatos temporales de la cámara.

La bitácora validó tres fechas reales:

```text
2026-05-28
2026-07-10
2026-08-21
```

Los demás criterios se utilizaron para asignar cada captura a una de esas sesiones registradas en bitácora:

- fuente: INTERNA o SD;
- carpeta original;
- nombre base;
- secuencia embebida;
- continuidad temporal.

Por tanto, estos criterios apoyan la **asignación y trazabilidad de capturas**, pero no generan nuevas fechas experimentales.

## 6. Dataset final

El resultado esperado es:

```text
Sesion_YYYY-MM-DD/
├── WebODM_Multiespectral/
└── RGB_Referencia/
```

Las capturas incompletas se mantienen fuera de `WebODM_Multiespectral`.

## 7. Trazabilidad

Se recomienda conservar siempre:

- nombre original;
- ruta original;
- fuente;
- carpeta original;
- SHA-256;
- ID normalizado de captura;
- fecha experimental final.


## 8. Estado de validación por sesión

El flujo completo de reconstrucción SfM, control de escala, calibración radiométrica, ortomosaico multibanda y validación inicial de índices ha sido comprobado hasta ahora en la sesión:

```text
2026-08-21
```

Las sesiones **2026-05-28** y **2026-07-10** permanecen pendientes de replicación completa. En consecuencia, todavía no debe asumirse que todos los parámetros, errores geométricos, respuestas radiométricas o decisiones de control de calidad observadas el 21 de agosto se reproducirán de forma idéntica en las otras fechas.

La comparación temporal entre sesiones se realizará únicamente después de aplicar el mismo flujo y los mismos criterios de control de calidad a las tres fechas.

## 9. Propósito analítico posterior

El flujo actual tiene como objetivo producir variables espectrales y geométricas trazables que puedan utilizarse posteriormente en una propuesta de **aprendizaje automático (ML)**.

La etapa de ML no forma parte todavía del flujo validado. Se considera una fase posterior, condicionada a:

- completar las tres sesiones;
- validar la consistencia radiométrica entre fechas;
- definir la unidad de análisis, por ejemplo planta individual o parcela;
- extraer estadísticas de índices por unidad experimental;
- disponer de variables objetivo o etiquetas apropiadas;
- separar adecuadamente datos de entrenamiento, validación y prueba para evitar fuga de información entre fechas o plantas.

Los índices actualmente considerados como candidatos de entrada son NDVI y GNDVI; EVI2 puede incorporarse una vez estandarizado su cálculo. NDRE permanece en revisión radiométrica.
