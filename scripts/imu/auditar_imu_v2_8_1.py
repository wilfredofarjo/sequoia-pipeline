#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auditar_imu_v2_8_1.py

Audita metadatos IMU/GPS de TIFF Parrot Sequoia mediante ExifTool.
No modifica archivos originales.

Salidas:
- imu_metadata_archivos_v281.csv
- imu_capturas_resumen_v281.csv
"""

from __future__ import annotations
import argparse, json, math, re, shutil, subprocess
from pathlib import Path
import pandas as pd

PATRON = re.compile(r"(?P<cap>CAP_\d+)_(?P<banda>GRE|RED|REG|NIR)(?:_\d+)?\.TIF$", re.I)

def buscar_clave(d, sufijos):
    for k,v in d.items():
        kl=k.lower()
        if any(kl.endswith(s.lower()) for s in sufijos):
            return v
    return None

def a_float(v):
    try:
        return float(v)
    except Exception:
        return math.nan

def estado_gps(v):
    if v is None:
        return ""
    s=str(v).strip().upper()
    if s in {"V","MEASUREMENT VOID"}: return "Measurement Void"
    if s in {"A","MEASUREMENT ACTIVE"}: return "Measurement Active"
    return str(v)

def delta_circular(valores):
    vals=[float(v)%360 for v in valores if pd.notna(v)]
    if len(vals)<2: return 0.0
    vals=sorted(vals)
    gaps=[vals[i+1]-vals[i] for i in range(len(vals)-1)] + [360-(vals[-1]-vals[0])]
    return 360-max(gaps)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--base", required=True, help="Carpeta raíz con TIFF Sequoia")
    ap.add_argument("--reportes", default="Sequoia_Organizado/Reportes")
    ap.add_argument("--tolerancia-grados", type=float, default=1.0)
    args=ap.parse_args()

    if not shutil.which("exiftool"):
        raise SystemExit("ERROR: ExifTool no está disponible en PATH.")

    base=Path(args.base)
    reportes=Path(args.reportes)
    reportes.mkdir(parents=True, exist_ok=True)

    archivos=[p for p in base.rglob("*") if p.is_file() and p.suffix.lower() in {".tif",".tiff"} and ".thumb" not in str(p).lower()]
    if not archivos:
        raise SystemExit("No se encontraron TIFF.")

    cmd=["exiftool","-j","-n",
         "-XMP:CameraYawDegree","-XMP:CameraPitchDegree","-XMP:CameraRollDegree",
         "-XMP:Yaw","-XMP:Pitch","-XMP:Roll",
         "-GPSStatus","-GPSLatitude","-GPSLongitude","-GPSAltitude"] + [str(p) for p in archivos]
    meta=json.loads(subprocess.check_output(cmd, text=True, errors="replace"))

    filas=[]
    for d in meta:
        p=Path(d.get("SourceFile",""))
        m=PATRON.search(p.name)
        if not m: continue
        filas.append({
            "archivo":str(p),
            "nombre":p.name,
            "capture_id":m.group("cap").upper(),
            "banda":m.group("banda").upper(),
            "yaw_deg":a_float(buscar_clave(d,["CameraYawDegree","Yaw"])),
            "pitch_deg":a_float(buscar_clave(d,["CameraPitchDegree","Pitch"])),
            "roll_deg":a_float(buscar_clave(d,["CameraRollDegree","Roll"])),
            "gps_status":estado_gps(buscar_clave(d,["GPSStatus"])),
            "gps_lat":a_float(buscar_clave(d,["GPSLatitude"])),
            "gps_lon":a_float(buscar_clave(d,["GPSLongitude"])),
            "gps_alt":a_float(buscar_clave(d,["GPSAltitude"])),
        })

    df=pd.DataFrame(filas).sort_values(["capture_id","banda"])
    df.to_csv(reportes/"imu_metadata_archivos_v281.csv", index=False)

    resumen=[]
    for cap,g in df.groupby("capture_id"):
        bandas=set(g["banda"])
        completas={"GRE","RED","REG","NIR"}.issubset(bandas)
        ypr=g[["yaw_deg","pitch_deg","roll_deg"]].notna().all(axis=1)
        con_ypr=int(ypr.sum())
        dy=delta_circular(g["yaw_deg"])
        dp=float(g["pitch_deg"].max()-g["pitch_deg"].min()) if g["pitch_deg"].notna().any() else math.nan
        dr=float(g["roll_deg"].max()-g["roll_deg"].min()) if g["roll_deg"].notna().any() else math.nan
        consistente=completas and con_ypr>=4 and max(dy,dp,dr)<=args.tolerancia_grados
        resumen.append({
            "capture_id":cap,
            "n_archivos":len(g),
            "bandas":";".join(sorted(bandas)),
            "captura_completa":completas,
            "n_bandas_ypr":con_ypr,
            "delta_yaw_deg":dy,
            "delta_pitch_deg":dp,
            "delta_roll_deg":dr,
            "consistente_1deg":consistente,
            "gps_measurement_void":bool((g["gps_status"]=="Measurement Void").any()),
            "tiene_gps_xy":bool(g["gps_lat"].notna().any() and g["gps_lon"].notna().any()),
        })
    rd=pd.DataFrame(resumen)
    rd.to_csv(reportes/"imu_capturas_resumen_v281.csv", index=False)

    print("="*72)
    print("AUDITORÍA IMU v2.8.1")
    print("="*72)
    print(f"Archivos TIFF auditados: {len(df)}")
    print(f"Capturas auditadas: {len(rd)}")
    print(f"Capturas completas: {int(rd.captura_completa.sum())}")
    print(f"Capturas consistentes <= {args.tolerancia_grados:.1f}°: {int(rd.consistente_1deg.sum())}")
    print(f"Capturas con GPS XY: {int(rd.tiene_gps_xy.sum())}")
    print(f"Capturas Measurement Void: {int(rd.gps_measurement_void.sum())}")
    print(f"Reportes: {reportes}")

if __name__=="__main__":
    main()
