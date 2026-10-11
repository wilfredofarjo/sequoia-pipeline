# Validación SfM–IMU

## Objetivo

Evaluar la coherencia entre las orientaciones registradas por la IMU de Parrot Sequoia y la orientación estimada de manera independiente mediante SfM en Metashape.

Esta validación es diagnóstica. No se utiliza la IMU como referencia durante la alineación SfM.

## Hallazgos de metadatos

La auditoría de TIFF mostró:

- coordenadas GPS XY no disponibles;
- `GPSStatus = Measurement Void`;
- Yaw, Pitch y Roll presentes para la mayoría de capturas;
- fechas internas de cámara no confiables.

Por esta razón, la bitácora de campo se mantiene como fuente de verdad temporal.

## Inventario IMU

- capturas auditadas: 674
- capturas con algún Yaw/Pitch/Roll: 648
- capturas consistentes entre bandas dentro de 1°: 644
- capturas completas utilizadas como núcleo estable: 644

## Evolución del análisis

```text
v2.8.1  auditoría de Yaw/Pitch/Roll
v2.8.2  candidatos de mapeo de ejes
v2.8.3b comparación Euler SfM–IMU
v2.8.4  validación mediante matrices de rotación
v2.8.4a exportación de camera.transform nativa
v2.8.5  comparación SO(3) con rotaciones nativas
```

## Correspondencia de imágenes

Para la sesión 2026-08-21:

- filas SfM alineadas: 564 cámaras individuales
- cámaras GRE seleccionadas: 141
- pares SfM–IMU coincidentes: 141
- etiquetas sin coincidencia: 0

Esto descarta un problema de asociación entre capturas como causa principal de las discrepancias angulares.

## Resultado v2.8.4

Mejor modelo matricial:

```text
Orden Euler: yaw > roll > pitch
Modo Euler: extrínseco
Lado boresight: left
Signos IMU: +Yaw, +Pitch, +Roll

error angular mediano: 10.501°
error angular medio:   10.888°
RMSE:                  11.472°
P95:                   17.030°
máximo:                19.737°
```

## Resultado v2.8.5

La v2.8.5 utiliza directamente las matrices derivadas de `camera.transform`.

```text
pares coincidentes: 141
error angular mediano: 10.435°
error angular medio:   10.451°
RMSE:                  11.099°
P95:                   16.762°
máximo:                19.788°
```

La mejora frente a v2.8.4 fue pequeña.

## Interpretación

El residual de aproximadamente 10° no debe interpretarse como:

- error directo del IMU;
- error directo de SfM;
- boresight físico definitivo.

El boresight estimado permanece cercano a 180°, lo que indica que la transformación incluye cambios de frame y convenciones de ejes además de una posible desalineación física.

## Estado

La relación absoluta SfM–IMU se considera **experimental y no resuelta completamente**.

La reconstrucción geométrica no depende de esta validación y puede continuar de forma independiente.

## Próxima validación recomendada

Comparar rotaciones relativas entre pares de imágenes consecutivas para evaluar si IMU y SfM describen el mismo movimiento angular sin depender de orientación absoluta, norte, ENU/NED, offsets constantes o boresight.
