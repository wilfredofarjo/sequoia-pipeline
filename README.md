# Sequoia WebODM Pipeline

Flujo reproducible para organizar, auditar, reconstruir y analizar imágenes multiespectrales **Parrot Sequoia** mediante **WebODM / OpenDroneMap** y **Agisoft Metashape**.

## Alcance

El proyecto nació como un organizador seguro de imágenes almacenadas entre la memoria interna de la cámara y la tarjeta SD, con fechas internas incorrectas y múltiples reinicios del reloj. La versión en desarrollo amplía ese flujo hacia:

- inventario y organización de imágenes;
- identificación de bandas `GRE`, `RED`, `REG`, `NIR` y RGB;
- detección de duplicados mediante SHA-256;
- reconstrucción de sesiones reales usando como referencia las fechas registradas en bitácora, no las fechas embebidas de la cámara;
- preparación de datasets multiespectrales para WebODM;
- reconstrucción SfM independiente en Agisoft Metashape;
- control geométrico mediante barras de escala;
- auditoría y comparación SfM–IMU (**Inertial Measurement Unit / Unidad de Medición Inercial**) como referencia complementaria de orientación ante la ausencia de coordenadas GPS XY válidas;
- calibración radiométrica con panel de reflectancia;
- generación de ortomosaicos multibanda;
- cálculo y validación de índices espectrales.

## Caso de estudio

| Fecha real | Capturas completas | TIFF multiespectrales |
|---|---:|---:|
| 2026-05-28 | 177 | 708 |
| 2026-07-10 | 314 | 1,256 |
| 2026-08-21 | 153 | 612 |
| **Total** | **644** | **2,576** |

Cada captura completa contiene cuatro bandas:

```text
GRE.TIF
RED.TIF
REG.TIF
NIR.TIF
```

Los archivos RGB se conservan como referencia y no se mezclan con el dataset multiespectral principal.

## Arquitectura del flujo

```text
TIFF originales de Sequoia
      │
      ▼
Organización + auditoría
      │
      ├── inventario
      ├── hashes / duplicados
      ├── agrupación multibanda
      └── asignación de sesión real
      │
      ├──────────────► WebODM / OpenDroneMap
      │
      ▼
Agisoft Metashape
      │
      ├── importación multicámara
      ├── alineación SfM
      ├── control de escala
      ├── mapas de profundidad / nube de puntos / malla
      ├── validación experimental SfM–IMU
      ├── calibración radiométrica
      └── ortomosaico multibanda
      │
      ▼
Análisis espectral
      ├── NDVI
      ├── GNDVI
      └── EVI2
```

## Estado actual

- [x] Organización de datos y detección de duplicados
- [x] Reconstrucción de sesiones reales
- [x] Dataset multiespectral para WebODM
- [x] Reconstrucción SfM validada para 2026-08-21
- [x] Control de escala mediante barras de escala
- [x] Exportación de rotaciones nativas de Metashape
- [x] Validación SfM–IMU preliminar
- [x] Calibración radiométrica con panel
- [x] Ortomosaico de 4 bandas
- [x] NDVI funcional
- [x] GNDVI disponible
- [ ] EVI2 como producto estándar
- [ ] Validación específica del canal Red Edge / NDRE
- [ ] Repetición completa para mayo y julio
- [ ] Validación completa de las sesiones 2026-05-28 y 2026-07-10
- [ ] Comparación temporal entre sesiones
- [ ] Segmentación por planta y extracción de estadísticas
- [ ] Propuesta de aprendizaje automático (ML) a partir de índices y variables derivadas

## Estructura del repositorio

```text
sequoia-webodm-pipeline/
├── README.md
├── .gitignore
├── scripts/
│   ├── README.md
│   ├── sequoia_dataset_organizer.py
│   ├── imu/
│   └── metashape/
├── docs/
│   ├── workflow.md
│   ├── webodm_configuration.md
│   ├── flujo_metashape.md
│   ├── validacion_sfm_imu.md
│   ├── calibracion_radiometrica.md
│   ├── indices_vegetacion.md
│   └── limitaciones.md
├── examples/
│   ├── session_mapping.example.json
│   └── session_mapping_by_folder.example.json
└── config/
    ├── panel_reflectancia_batch4001.csv
    └── parametros_metashape.yaml
```

## Requisitos básicos

### Organización del dataset

- Python 3.9 o superior
- El organizador principal no requiere paquetes externos.

### Reconstrucción y análisis

- Agisoft Metashape Professional 2.2
- ExifTool para auditorías de metadatos
- Python 3 para scripts auxiliares de validación

## Uso del organizador

La carpeta base debe contener:

```text
Fotos Parrot Sequoia/
├── Interna/
└── SD/
```

### Diagnóstico

```bash
python3 scripts/sequoia_dataset_organizer.py \
  --base "/ruta/Fotos Parrot Sequoia"
```

### Asignación de fechas mediante bitácora

```bash
python3 scripts/sequoia_dataset_organizer.py \
  --base "/ruta/Fotos Parrot Sequoia" \
  --session-map examples/session_mapping_by_folder.example.json
```

### Crear dataset final

```bash
python3 scripts/sequoia_dataset_organizer.py \
  --base "/ruta/Fotos Parrot Sequoia" \
  --session-map examples/session_mapping_by_folder.example.json \
  --copy-final
```

## Documentación metodológica

- [Flujo general](docs/workflow.md)
- [Configuración de WebODM](docs/webodm_configuration.md)
- [Reconstrucción SfM en Metashape](docs/flujo_metashape.md)
- [Validación SfM–IMU](docs/validacion_sfm_imu.md)
- [Calibración radiométrica](docs/calibracion_radiometrica.md)
- [Índices de vegetación](docs/indices_vegetacion.md)
- [Limitaciones y decisiones metodológicas](docs/limitaciones.md)
- [Diagrama y registro de decisiones metodológicas](docs/decisiones_metodologicas.md)
- [Referencias y documentos utilizados](docs/referencias.md)

## Principio de seguridad de datos

Los archivos originales no se renombran, no se mueven y no se modifican. El pipeline trabaja mediante inventarios, hashes, metadatos y copias hacia carpetas nuevas.

## Datos no incluidos

El repositorio no contiene TIFF/JPG originales, archivos `.DAT`, proyectos `.psx`, nubes de puntos completas ni ortomosaicos de gran tamaño.

## Versionado

- **v0.1.0** — organización y preparación del dataset para WebODM.
- **v0.2.0** — SfM en Metashape, validación IMU, calibración radiométrica y análisis espectral inicial.
- **v0.3.0 (en desarrollo)** — scripts reproducibles, decisiones metodológicas explícitas, validación multi-sesión y preparación para análisis ML.


## Alcance de la validación

Hasta el momento, el flujo completo ha sido validado únicamente para la sesión **2026-08-21**. Las sesiones **2026-05-28** y **2026-07-10** deben reproducir el mismo procedimiento antes de realizar inferencias temporales o entrenar modelos de aprendizaje automático.

El objetivo futuro es generar una propuesta de **ML** basada en índices espectrales y variables derivadas del fenotipado. Esa etapa se considera posterior y dependerá de la consistencia entre sesiones, la definición de unidades experimentales y la disponibilidad de variables objetivo.
