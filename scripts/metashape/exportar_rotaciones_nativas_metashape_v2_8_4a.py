# -*- coding: utf-8 -*-
"""
exportar_rotaciones_nativas_metashape_v2_8_4a.py

Ejecutar DENTRO de Agisoft Metashape Professional.
Exporta la matriz 3x3 nativa de camera.transform para cada cámara alineada.

Salida:
- metashape_native_rotations_v284a.csv

La exportación conserva la rotación nativa y evita convertir primero a Euler.
"""

import csv
from pathlib import Path
import Metashape

doc=Metashape.app.document
chunk=doc.chunk
if chunk is None: raise RuntimeError("No hay chunk activo.")
if not doc.path: raise RuntimeError("Guarde primero el proyecto .psx.")

out=Path(doc.path).parent/"metashape_native_rotations_v284a.csv"
campos=["label","sensor","master_gre",
        "r11","r12","r13","r21","r22","r23","r31","r32","r33"]
filas=[]
for cam in chunk.cameras:
    if cam.transform is None: continue
    R=cam.transform.rotation()
    filas.append({
        "label":cam.label,
        "sensor":cam.sensor.label if cam.sensor else "",
        "master_gre":int("_GRE" in cam.label.upper()),
        "r11":R[0,0],"r12":R[0,1],"r13":R[0,2],
        "r21":R[1,0],"r22":R[1,1],"r23":R[1,2],
        "r31":R[2,0],"r32":R[2,1],"r33":R[2,2],
    })

with open(out,"w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=campos); w.writeheader(); w.writerows(filas)

print("="*72)
print("EXPORTACIÓN ROTACIONES NATIVAS METASHAPE v2.8.4a")
print("="*72)
print("Filas exportadas:",len(filas))
print("Archivo:",out)
print("[OK] Exportación completada.")
