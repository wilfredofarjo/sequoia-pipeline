# Scripts del pipeline

Esta carpeta contiene las versiones públicas y reproducibles del flujo desarrollado durante la organización, reconstrucción SfM y validación IMU del proyecto Parrot Sequoia.

## Principio de versionado

Las versiones v2.8.x reflejan la evolución metodológica del análisis. No representan únicamente correcciones de código: cada salto incorpora una pregunta de control diferente.

### Organización estable

`sequoia_dataset_organizer.py`

Versión pública derivada del flujo estable v2.7:
- inventario;
- SHA-256;
- duplicados;
- agrupación multibanda;
- asignación por sesión;
- preparación de dataset final.

## Auditoría IMU

En este repositorio, **IMU** significa **Inertial Measurement Unit** (**Unidad de Medición Inercial**). Su uso se incorporó porque las imágenes auditadas no disponían de coordenadas GPS XY válidas (`GPSStatus = Measurement Void`). Ante esa ausencia, se aprovecharon los metadatos de **orientación** registrados por el equipo —principalmente **Yaw, Pitch y Roll**— como información complementaria para contrastar la orientación estimada de forma independiente mediante SfM en Metashape. Estos datos IMU no sustituyen al GPS ni proporcionan por sí solos una posición absoluta XY; describen la actitud/orientación del sensor.

### v2.8.1 — `imu/auditar_imu_v2_8_1.py`

Audita Yaw/Pitch/Roll, estado GPS y consistencia entre bandas.

Ejemplo:

```bash
python3 scripts/imu/auditar_imu_v2_8_1.py \
  --base "/ruta/Fotos Parrot Sequoia"
```

### v2.8.2 — `imu/preparar_mapeo_ejes_v2_8_2.py`

Resume una orientación por captura completa y genera el mapeo candidato de ejes para Metashape.

Los signos y el boresight siguen marcados como no validados.

## Exportación desde Metashape

### v2.8.3a — `metashape/exportar_sfm_metashape_v2_8_3a.py`

Se ejecuta **dentro de Metashape**.

Exporta Yaw/Pitch/Roll estimados para comparación diagnóstica.

### v2.8.4a — `metashape/exportar_rotaciones_nativas_metashape_v2_8_4a.py`

Se ejecuta **dentro de Metashape**.

Exporta directamente la matriz 3×3 de `camera.transform`. Esta es la exportación recomendada para la validación moderna porque evita convertir primero a Euler.

## Validación SfM–IMU

### v2.8.3b — `imu/validar_sfm_imu_v2_8_3b.py`

Diagnóstico Euler:
- prueba signos;
- estima offsets circulares;
- genera residuales.

No debe usarse para establecer un boresight físico definitivo.

### v2.8.4 — `imu/validar_sfm_imu_v2_8_4.py`

Convierte las orientaciones a matrices y explora órdenes Euler, modos, signos y lado del boresight.

Se conserva como etapa intermedia de la evolución del análisis.

### v2.8.5 — `imu/validar_sfm_imu_v2_8_5.py`

**Versión recomendada para validación absoluta experimental.**

Usa rotaciones nativas de Metashape y compara modelos en SO(3), incluyendo cambios de frame.

## Dependencias

Los scripts ejecutados desde terminal requieren:

```bash
python3 -m pip install numpy pandas scipy
```

Además, `auditar_imu_v2_8_1.py` requiere ExifTool disponible en `PATH`.

Los scripts bajo `scripts/metashape/` deben ejecutarse con el intérprete Python integrado de Agisoft Metashape y no requieren instalación de `Metashape` mediante pip.

## Orden recomendado de ejecución

```text
sequoia_dataset_organizer.py
        ↓
auditar_imu_v2_8_1.py
        ↓
preparar_mapeo_ejes_v2_8_2.py
        ↓
Reconstrucción SfM independiente en Metashape
        ↓
exportar_sfm_metashape_v2_8_3a.py
        ↓
validar_sfm_imu_v2_8_3b.py
        ↓
validar_sfm_imu_v2_8_4.py
        ↓
exportar_rotaciones_nativas_metashape_v2_8_4a.py
        ↓
validar_sfm_imu_v2_8_5.py
```

Para nuevas sesiones, v2.8.3b y v2.8.4 pueden omitirse si únicamente se desea la validación nativa final; se mantienen porque documentan la evolución metodológica.

## Advertencia de reproducibilidad

Estas son versiones públicas reconstruidas y ordenadas a partir del flujo validado del proyecto. Mantienen la lógica y los productos esperados, pero no deben asumirse byte-a-byte idénticas a todas las versiones locales intermedias ejecutadas durante el desarrollo.
