# -*- coding: utf-8 -*-
"""
exportar_sfm_metashape_v2_8_3a.py

Ejecutar DENTRO de Agisoft Metashape Professional.
Exporta orientaciones SfM estimadas de cámaras alineadas a CSV.

Salidas, en la carpeta del proyecto .psx:
- metashape_sfm_orientations_v283.csv      (solo cámaras master/GRE alineadas)
- metashape_sfm_all_aligned_v283a.csv      (todas las cámaras alineadas)

No importa IMU ni modifica la alineación.
"""

import csv
from pathlib import Path
import Metashape

doc = Metashape.app.document
chunk = doc.chunk
if chunk is None:
    raise RuntimeError("No hay un chunk activo.")
if not doc.path:
    raise RuntimeError("Guarde primero el proyecto .psx para definir la carpeta de salida.")

outdir = Path(doc.path).parent
csv_gre = outdir / "metashape_sfm_orientations_v283.csv"
csv_all = outdir / "metashape_sfm_all_aligned_v283a.csv"

def matriz_mundo_camara(cam):
    # Transformación del sistema interno del chunk al frame local del chunk.
    return chunk.transform.matrix * cam.transform

def ypr_desde_transform(cam):
    T = matriz_mundo_camara(cam)
    R = T.rotation()
    # Metashape devuelve Yaw/Pitch/Roll en grados.
    ypr = Metashape.utils.mat2ypr(R)
    return float(ypr[0]), float(ypr[1]), float(ypr[2])

filas=[]
for cam in chunk.cameras:
    if cam.transform is None:
        continue
    try:
        yaw,pitch,roll=ypr_desde_transform(cam)
    except Exception as e:
        print("WARN:", cam.label, e)
        continue
    filas.append({
        "label":cam.label,
        "yaw_sfm_deg":yaw,
        "pitch_sfm_deg":pitch,
        "roll_sfm_deg":roll,
        "sensor":cam.sensor.label if cam.sensor else "",
        "master_gre": int("_GRE" in cam.label.upper())
    })

campos=["label","yaw_sfm_deg","pitch_sfm_deg","roll_sfm_deg","sensor","master_gre"]

with open(csv_all,"w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=campos)
    w.writeheader(); w.writerows(filas)

gre=[r for r in filas if r["master_gre"]==1]
with open(csv_gre,"w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=campos)
    w.writeheader(); w.writerows(gre)

print("="*72)
print("EXPORTACIÓN SfM METASHAPE v2.8.3a")
print("="*72)
print("Cámaras totales en chunk:", len(chunk.cameras))
print("Cámaras con transform/alineadas:", len(filas))
print("Cámaras GRE alineadas:", len(gre))
print()
print("CSV GRE:", csv_gre)
print("CSV diagnóstico:", csv_all)
print("[OK] Exportación completada.")
