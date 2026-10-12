#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validar_sfm_imu_v2_8_3b.py

Comparación diagnóstica de orientaciones SfM (Euler) e IMU.
Busca las 8 combinaciones de signo y estima offsets circulares por eje.

IMPORTANTE:
- Es un diagnóstico de convenciones Euler.
- Los offsets NO deben interpretarse como boresight físico definitivo.
"""

from __future__ import annotations
import argparse, itertools, math, re
from pathlib import Path
import numpy as np
import pandas as pd

def wrap180(x):
    return (np.asarray(x,dtype=float)+180.0)%360.0-180.0

def mediana_circular_deg(x):
    x=np.asarray(x,dtype=float)
    # offset robusto alrededor de la mediana lineal envuelta
    c=np.angle(np.mean(np.exp(1j*np.deg2rad(x))),deg=True)
    return float(c)

def normalizar_id(s):
    m=re.search(r"(CAP_\d+)", str(s).upper())
    return m.group(1) if m else str(s).strip().upper()

def leer_sfm(path):
    df=pd.read_csv(path)
    cmap={c.lower():c for c in df.columns}
    def pick(*opts):
        for o in opts:
            if o.lower() in cmap: return cmap[o.lower()]
        raise KeyError("No se encontró columna: "+"/".join(opts))
    label=pick("label","camera","name")
    yaw=pick("yaw_sfm_deg","yaw","yaw est","yaw_est")
    pitch=pick("pitch_sfm_deg","pitch","pitch est","pitch_est")
    roll=pick("roll_sfm_deg","roll","roll est","roll_est")
    x=df[[label,yaw,pitch,roll]].copy()
    x.columns=["label","yaw_sfm","pitch_sfm","roll_sfm"]
    x["capture_id"]=x["label"].map(normalizar_id)
    # si hay bandas individuales, usar master GRE
    mask=x["label"].astype(str).str.contains("_GRE",case=False,regex=False)
    if mask.any(): x=x[mask].copy()
    return x, (label,yaw,pitch,roll)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--imu", default="Sequoia_Organizado/Reportes/metashape_axis_mapping_candidates_v282.csv")
    ap.add_argument("--sfm", default="Sequoia_Organizado/Reportes/metashape_sfm_all_aligned_v283a.csv")
    ap.add_argument("--reportes", default="Sequoia_Organizado/Reportes")
    args=ap.parse_args()

    imu=pd.read_csv(args.imu)
    sfm,cols=leer_sfm(args.sfm)
    imu["capture_id"]=imu["capture_id"].map(normalizar_id)

    merged=sfm.merge(imu,on="capture_id",how="inner",suffixes=("","_imu"))
    if merged.empty: raise SystemExit("No hay pares SfM–IMU coincidentes.")

    # v2.8.2 ya contiene el mapeo candidato de ejes en convención Metashape
    src=["yaw_ms_candidate_deg","pitch_ms_candidate_deg","roll_ms_candidate_deg"]
    dst=["yaw_sfm","pitch_sfm","roll_sfm"]

    pruebas=[]
    residuales_mejor=None
    best=None
    for signs in itertools.product([1,-1], repeat=3):
        offsets=[]; resids=[]
        for s,si,di in zip(src,signs,dst):
            raw=wrap180(merged[di].to_numpy()-si*merged[s].to_numpy())
            off=mediana_circular_deg(raw)
            resid=wrap180(raw-off)
            offsets.append(off); resids.append(resid)
        A=np.vstack(resids).T
        score=np.median(np.sqrt(np.mean(A*A,axis=1)))
        row={
            "sign_yaw":signs[0],"sign_pitch":signs[1],"sign_roll":signs[2],
            "offset_yaw_deg":offsets[0],"offset_pitch_deg":offsets[1],"offset_roll_deg":offsets[2],
            "score_mediano_combinado_deg":score
        }
        pruebas.append(row)
        if best is None or score<best["score_mediano_combinado_deg"]:
            best=row; residuales_mejor=A.copy()

    rep=Path(args.reportes); rep.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(pruebas).sort_values("score_mediano_combinado_deg").to_csv(rep/"sfm_imu_sign_tests_v283.csv",index=False)
    pd.DataFrame([best]).to_csv(rep/"sfm_imu_best_global_v283.csv",index=False)

    rr=merged[["capture_id","label"]].copy()
    rr["resid_yaw_deg"]=residuales_mejor[:,0]
    rr["resid_pitch_deg"]=residuales_mejor[:,1]
    rr["resid_roll_deg"]=residuales_mejor[:,2]
    rr["error_combinado_deg"]=np.sqrt(np.mean(residuales_mejor**2,axis=1))
    rr.to_csv(rep/"sfm_imu_residuals_best_v283.csv",index=False)

    score=best["score_mediano_combinado_deg"]
    qc="COHERENCIA_ALTA" if score<3 else ("COHERENCIA_INTERMEDIA_REVISAR_BORESIGHT" if score<8 else "COHERENCIA_BAJA_REVISAR_MODELO")

    print("="*72); print("VALIDACIÓN SfM–IMU v2.8.3b"); print("="*72)
    print("Candidatos IMU v2.8.2:",len(imu))
    print("Filas SfM leídas:",len(pd.read_csv(args.sfm)))
    print(f"Columnas detectadas: label={cols[0]}, yaw={cols[1]}, pitch={cols[2]}, roll={cols[3]}")
    print("Filas GRE seleccionadas automáticamente:",len(sfm))
    print("Pares SfM–IMU coincidentes:",len(merged))
    print()
    print("MEJOR COMBINACIÓN GLOBAL (diagnóstico)")
    print("-"*72)
    print(f"Signos: Yaw={best['sign_yaw']:+d}, Pitch={best['sign_pitch']:+d}, Roll={best['sign_roll']:+d}")
    print(f"Offsets: Yaw={best['offset_yaw_deg']:.3f}°, Pitch={best['offset_pitch_deg']:.3f}°, Roll={best['offset_roll_deg']:.3f}°")
    print(f"Score mediano combinado: {score:.3f}°")
    print("QC:",qc)
    print("\nIMPORTANTE: no usar estos offsets como boresight definitivo.")

if __name__=="__main__":
    main()
