#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
preparar_mapeo_ejes_v2_8_2.py

Resume Yaw/Pitch/Roll por captura completa y genera el archivo candidato
para comparación posterior con Metashape.

Mapeo candidato documentado:
- Metashape Yaw   <- Parrot Yaw
- Metashape Pitch <- Parrot Roll
- Metashape Roll  <- Parrot Pitch

Los signos y el boresight NO se consideran validados en esta etapa.
"""

from __future__ import annotations
import argparse, math, re
from pathlib import Path
import numpy as np
import pandas as pd

def media_circular(grados):
    a=np.deg2rad(np.asarray(grados,dtype=float))
    return float(np.rad2deg(np.arctan2(np.mean(np.sin(a)),np.mean(np.cos(a)))) % 360)

def inferir_sesion(rutas):
    for r in rutas:
        m=re.search(r"(20\d{2}-\d{2}-\d{2})", str(r))
        if m: return m.group(1)
    return ""

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--metadata", default="Sequoia_Organizado/Reportes/imu_metadata_archivos_v281.csv")
    ap.add_argument("--salida", default="Sequoia_Organizado/Reportes/metashape_axis_mapping_candidates_v282.csv")
    ap.add_argument("--tolerancia-grados", type=float, default=1.0)
    args=ap.parse_args()

    df=pd.read_csv(args.metadata)
    out=[]
    for cap,g in df.groupby("capture_id"):
        g4=g[g["banda"].isin(["GRE","RED","REG","NIR"])].copy()
        if set(g4["banda"]) != {"GRE","RED","REG","NIR"}: continue
        if not g4[["yaw_deg","pitch_deg","roll_deg"]].notna().all().all(): continue

        yaw=media_circular(g4["yaw_deg"])
        pitch=float(g4["pitch_deg"].mean())
        roll=float(g4["roll_deg"].mean())

        dy=max(abs(((g4["yaw_deg"]-yaw+180)%360)-180))
        dp=float((g4["pitch_deg"]-pitch).abs().max())
        dr=float((g4["roll_deg"]-roll).abs().max())
        estado="CONSISTENTE_ENTRE_BANDAS" if max(dy,dp,dr)<=args.tolerancia_grados else "REVISAR_DELTA_BANDAS"

        gre=g4[g4["banda"]=="GRE"].iloc[0]
        out.append({
            "capture_id":cap,
            "label":cap,
            "gre_filename":gre["nombre"],
            "sesion":inferir_sesion(g4["archivo"]),
            "yaw_parrot_deg":yaw,
            "pitch_parrot_deg":pitch,
            "roll_parrot_deg":roll,
            "yaw_ms_candidate_deg":yaw,
            "pitch_ms_candidate_deg":roll,
            "roll_ms_candidate_deg":pitch,
            "delta_max_band_deg":max(dy,dp,dr),
            "consistency_status":estado,
            "sign_status":"NO_VALIDADO",
            "boresight_mount_status":"NO_VALIDADO",
            "import_status":"NO_IMPORTAR_DIRECTAMENTE",
        })

    odf=pd.DataFrame(out).sort_values(["sesion","capture_id"])
    Path(args.salida).parent.mkdir(parents=True, exist_ok=True)
    odf.to_csv(args.salida,index=False)

    print("="*72)
    print("PREPARACIÓN MAPEO DE EJES v2.8.2")
    print("="*72)
    print(f"Capturas candidatas: {len(odf)}")
    print(odf["consistency_status"].value_counts(dropna=False).to_string())
    print(f"Salida: {args.salida}")

if __name__=="__main__":
    main()
