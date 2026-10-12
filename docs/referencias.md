# Referencias y documentos utilizados

Este documento reúne las fuentes técnicas y bibliográficas utilizadas para construir y justificar el flujo reproducible del repositorio.

## Documentación oficial de Parrot Sequoia

1. **Parrot. (2017). _Sequoia User Guide_, versión 1.1 (05/2017).**  
   Manual oficial del sensor Parrot Sequoia. Se utilizó para interpretar la arquitectura del sensor, las bandas multiespectrales, el Sunshine Sensor, la calibración del equipo, los metadatos disponibles y la convención de orientación Yaw/Pitch/Roll.  
   https://www.parrot.com/assets/s3fs-public/2021-09/sequoia-userguide-en-fr-es-de-it-pt-ar-zn-zh-jp-ko_1.pdf

2. **Parrot Support Center. _Documentation & downloads for legacy products: Sequoia_.**  
   Portal oficial de documentación del fabricante.  
   https://www.parrot.com/en/support/documentation

## Documentación oficial de Agisoft Metashape

3. **Agisoft LLC. (2025). _Agisoft Metashape User Manual — Professional Edition, Version 2.2_.**  
   Fuente principal para el flujo SfM, importación multicámara, alineación, scale bars, optimización, mapas de profundidad, malla, ortomosaico, exportación de referencias, cámaras y rotaciones, procesamiento multiespectral, calibración de reflectancia y Raster Calculator.  
   https://www.agisoft.com/pdf/metashape-pro_2_2_en.pdf

4. **Agisoft LLC. _Tutorials & FAQ — Radiometric calibration using reflectance panels_.**  
   Tutorial oficial para calibración de reflectancia con imágenes de panel, incluyendo sensores compatibles como Parrot Sequoia.  
   https://www.agisoft.com/support/tutorials/

5. **Agisoft LLC. _MicaSense Altum processing workflow (including Reflectance Calibration) in Agisoft Metashape Professional_.**  
   Aunque el ejemplo se presenta con MicaSense, la documentación oficial indica que el mismo flujo de carga multicámara y calibración de reflectancia es aplicable a Parrot Sequoia. Se utilizó como referencia complementaria para el manejo de imágenes de calibración, paneles y `Normalize band sensitivity`.  
   https://agisoft.freshdesk.com/support/solutions/articles/31000148381-micasense-altum-processing-workflow-including-reflectance-calibration-in-agisoft-metashape-professi

## Referencias para índices de vegetación

6. **Gitelson, A. A., Kaufman, Y. J., & Merzlyak, M. N. (1996). _Use of a green channel in remote sensing of global vegetation from EOS-MODIS_. Remote Sensing of Environment, 58(3), 289–298.**  
   DOI: https://doi.org/10.1016/S0034-4257(96)00072-7  
   Referencia utilizada para fundamentar el uso del canal Green y el índice GNDVI.

7. **Jiang, Z., Huete, A. R., Didan, K., & Miura, T. (2008). _Development of a two-band enhanced vegetation index without a blue band_. Remote Sensing of Environment, 112(10), 3833–3845.**  
   DOI: https://doi.org/10.1016/j.rse.2008.06.006  
   Referencia utilizada para justificar EVI2 como alternativa al EVI clásico cuando no se dispone de banda azul.

8. **Pérez-Chimal, R. J., Rivera-Romero, C. A., Estudillo-Ayala, J. M., Sandoval-Aréchiga, R., Barrientos-García, A., & Muñoz-Minjares, J. U. (2026). _Extraction of Plant Physiological Features Using Multispectral Imaging and Spectrophotometry: A Systematic Review Highlighting Research Gaps for Stenocereus spp._ AgriEngineering, 8, 162.**  
   DOI: https://doi.org/10.3390/agriengineering8050162  
   Utilizada para fundamentar la selección de NDVI, GNDVI, NDRE y bandas NIR/Red Edge, así como la necesidad de calibración radiométrica, control de iluminación y validación metodológica.

9. **Zandi, A., Hosseinirad, S., Kashani Zadeh, H., Tavakolian, K., Cho, B.-K., Vasefi, F., Kim, M. S., & Tavakolian, P. (2025). _A systematic review of multi-mode analytics for enhanced plant stress evaluation_. Frontiers in Plant Science, 16, 1545025.**  
   DOI: https://doi.org/10.3389/fpls.2025.1545025  
   Utilizada para relacionar NIR, Red Edge y otros modos espectrales con respuestas de estrés, cambios fisiológicos y síntomas estructurales de la planta.

10. **Haque, M. A., Reza, M. N., Ali, M., Karim, M. R., Ahmed, S., Lee, K.-D., Khang, Y. H., & Chung, S.-O. (2024). _Effects of Environmental Conditions on Vegetation Indices from Multispectral Images: A Review_. Korean Journal of Remote Sensing, 40(4), 319–341.**  
    DOI: https://doi.org/10.7780/kjrs.2024.40.4.1  
    Utilizada para fundamentar el uso comparado de NDVI, NDRE, GNDVI y EVI y para documentar la influencia de iluminación, ambiente y calibración sobre la reflectancia y los índices.

## Nota sobre NDVI y NDRE

El NDVI se utiliza en este repositorio como índice principal por su respuesta espacial coherente en el dataset validado. NDRE fue evaluado de forma exploratoria, pero quedó fuera del análisis cuantitativo principal debido a la relación radiométrica inesperada entre NIR y Red Edge observada en la sesión 2026-08-21.

La exclusión de NDRE no se basa en una modificación de su fórmula, sino en un criterio de control de calidad radiométrico documentado en:

- `docs/calibracion_radiometrica.md`
- `docs/limitaciones.md`

## Convenciones

Los nombres de comandos, parámetros o elementos de la interfaz de Metashape se mantienen en inglés cuando corresponden literalmente a la aplicación, por ejemplo:

- `Normalize band sensitivity`
- `Raster transform`
- `Reference preselection`
- `camera.transform`
- `Yaw / Pitch / Roll`

Esto evita ambigüedad entre la documentación del repositorio y la interfaz real del software.
