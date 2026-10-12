# Decisiones metodológicas y puntos de control

Este documento resume las principales dudas metodológicas que surgieron durante el desarrollo del flujo y la decisión adoptada en cada caso.

## Diagrama de decisiones

```mermaid
flowchart TD
    A[Imágenes Parrot Sequoia] --> B{¿Fecha EXIF confiable?}
    B -- No --> C[Usar fechas registradas en bitácora]
    C --> D[Asignar capturas a sesiones usando carpeta, fuente, secuencia y continuidad]

    D --> E{¿GPS XY válido?}
    E -- No --> F[Reconstrucción SfM en sistema local]
    F --> G[Usar dimensiones físicas del contenedor]
    G --> H[Crear marcadores CONT_A, CONT_B, CONT_C y CONT_D]
    H --> I[Crear barras de escala y optimizar]

    E -- No --> J[Auditar IMU: Yaw, Pitch y Roll]
    J --> K[Comparar orientación IMU con orientación SfM]
    K --> L[Usar comparación como diagnóstico, no como georreferenciación]

    I --> M[Calibración radiométrica con panel]
    M --> N[Ortomosaico multibanda]
    N --> O[Calcular NDVI y GNDVI]
    O --> P{¿Red Edge radiométricamente consistente?}
    P -- No --> Q[Excluir NDRE del análisis principal]
    P -- Sí --> R[Evaluar NDRE]

    Q --> S{¿Flujo replicado en las 3 sesiones?}
    R --> S
    S -- No --> T[No realizar todavía inferencia temporal ni ML definitivo]
    S -- Sí --> U[Comparación temporal]
    U --> V[Extracción de variables por planta o unidad experimental]
    V --> W[Propuesta de aprendizaje automático]
```

## Registro de decisiones

| Duda metodológica | Evidencia observada | Decisión adoptada | Consecuencia |
|---|---|---|---|
| Fechas internas no confiables | Reinicios del reloj y fechas incorrectas | Usar bitácora como referencia temporal | Las sesiones son 2026-05-28, 2026-07-10 y 2026-08-21 |
| Ausencia de GPS XY | `GPSStatus = Measurement Void` | Trabajar en coordenadas locales | No hay georreferenciación absoluta |
| Escala física del modelo | Contenedor medido el 22-05-2026 | Marcadores + barras de escala | El modelo obtiene escala métrica |
| Uso de IMU | Yaw/Pitch/Roll disponibles | Auditoría y comparación con SfM | Diagnóstico de orientación, no posición |
| CONT_C no es una esquina exacta | Punto físico parcialmente visible | Usarlo como referencia aproximada | Sus errores no son una validación métrica estricta |
| Panel de reflectancia | Batch 4001 disponible | Calibración por banda | Permite análisis espectral trazable |
| NDRE negativo | NIR < Red Edge en gran parte del mosaico | Excluir NDRE por ahora | Evita forzar una interpretación incorrecta |
| Validación entre fechas | Solo 2026-08-21 completada | Replicar mayo y julio | No hay todavía comparación temporal validada |
| ML | Variables espectrales aún no armonizadas entre fechas | Posponer entrenamiento | Primero validar las tres sesiones |

## Principio general

Cuando una fuente de información no es confiable o está ausente, el flujo no intenta reconstruirla artificialmente. Se documenta la limitación y se utiliza la fuente independiente más apropiada disponible, manteniendo separadas las funciones de tiempo, posición, orientación, escala y reflectancia.
