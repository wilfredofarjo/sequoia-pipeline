#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validar_sfm_imu_v2_8_4.py

Validación matricial SfM–IMU a partir de orientaciones Euler.
Explora órdenes Euler, modo intrínseco/extrínseco, signos y lado del boresight.

Requiere:
- numpy
- pandas
- scipy

IMPORTANTE:
Esta etapa sigue dependiendo de una representación Euler de entrada.
La validación con rotaciones nativas de Metashape se realiza en v2.8.5.
"""

from __future__ import annotations
import argparse, itertools, re
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation as R

def normalizar_id(s):
    m=re.search(r"(CAP_\d+)", str(s).upper())
    return m.group(1) if m else str(s).strip().upper()

def rot_media(mats):
    return R.from_matrix(np.asarray(mats)).mean().as_matrix()

def ang_error(A,B):
    rel=np.einsum("nij,njk->nik", np.transpose(A,(0,2,1)), B)
    tr=np.clip((np.trace(rel,axis1=1,axis2=2)-1)/2,-1,1)
    return np.rad2deg(np.arccos(tr))

def euler_matrix(yaw,pitch,roll,orden,modo,signos):
    vals={"yaw":yaw*signos[0],"pitch":pitch*signos[1],"roll":roll*signos[2]}
    seq="".join({"yaw":"z","pitch":"x","roll":"y"}[k] for k in orden)
    if modo=="intrinsic": seq=seq.upper()
    ang=np.column_stack([vals[k] for k in orden])
    return R.from_euler(seq,ang,degrees=True).as_matrix()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--imu",default="Sequoia_Organizado/Reportes/metashape_axis_mapping_candidates_v282.csv")
    ap.add_argument("--sfm",default="Sequoia_Organizado/Reportes/metashape_sfm_all_aligned_v283a.csv")
    ap.add_argument("--reportes",default="Sequoia_Organizado/Reportes")
    args=ap.parse_args()

    imu=pd.read_csv(args.imu); sfm=pd.read_csv(args.sfm)
    sfm=sfm[sfm["label"].astype(str).str.contains("_GRE",case=False,regex=False)].copy()
    sfm["capture_id"]=sfm["label"].map(normalizar_id)
    imu["capture_id"]=imu["capture_id"].map(normalizar_id)
    d=sfm.merge(imu,on="capture_id",how="inner")
    if d.empty: raise SystemExit("No hay pares coincidentes.")

    sfmR=R.from_euler("zxy",d[["yaw_sfm_deg","pitch_sfm_deg","roll_sfm_deg"]].to_numpy(),degrees=True).as_matrix()
    ordenes=list(itertools.permutations(["yaw","pitch","roll"]))
    modos=["extrinsic","intrinsic"]
    signos=list(itertools.product([1,-1],repeat=3))
    lados=["left","right"]

    modelos=[]; best=None; best_err=None; best_B=None
    for orden in ordenes:
        for modo in modos:
            for sig in signos:
                imuR=euler_matrix(d["yaw_parrot_deg"].to_numpy(),
                                  d["pitch_parrot_deg"].to_numpy(),
                                  d["roll_parrot_deg"].to_numpy(),
                                  orden,modo,sig)
                for lado in lados:
                    if lado=="left":
                        Bs=np.einsum("nij,njk->nik",sfmR,np.transpose(imuR,(0,2,1)))
                        B=rot_media(Bs)
                        pred=np.einsum("ij,njk->nik",B,imuR)
                    else:
                        Bs=np.einsum("nij,njk->nik",np.transpose(imuR,(0,2,1)),sfmR)
                        B=rot_media(Bs)
                        pred=np.einsum("nij,jk->nik",imuR,B)
                    err=ang_error(pred,sfmR)
                    row={
                        "orden":">".join(orden),"modo":modo,"boresight_side":lado,
                        "sign_yaw":sig[0],"sign_pitch":sig[1],"sign_roll":sig[2],
                        "mediana_deg":float(np.median(err)),
                        "media_deg":float(np.mean(err)),
                        "rmse_deg":float(np.sqrt(np.mean(err**2))),
                        "p95_deg":float(np.percentile(err,95)),
                        "max_deg":float(np.max(err)),
                    }
                    modelos.append(row)
                    if best is None or row["mediana_deg"]<best["mediana_deg"]:
                        best=row; best_err=err.copy(); best_B=B.copy()

    rep=Path(args.reportes); rep.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(modelos).sort_values("mediana_deg").to_csv(rep/"sfm_imu_modelos_v284.csv",index=False)
    pd.DataFrame([best]).to_csv(rep/"sfm_imu_mejor_modelo_v284.csv",index=False)
    rr=d[["capture_id","label"]].copy(); rr["error_angular_deg"]=best_err
    rr.to_csv(rep/"sfm_imu_residuales_v284.csv",index=False)
    np.savetxt(rep/"boresight_matrix_v284.csv",best_B,delimiter=",")

    qc="COHERENCIA_ALTA" if best["mediana_deg"]<3 else ("COHERENCIA_INTERMEDIA_REVISAR_BORESIGHT" if best["mediana_deg"]<8 else "COHERENCIA_BAJA_REVISAR_MODELO")

    print("="*76)
    print("VALIDACIÓN MATRICIAL SfM–IMU v2.8.4")
    print("="*76)
    print("Pares SfM–IMU coincidentes:",len(d))
    print("Modelos probados:",len(modelos))
    print("\nMEJOR MODELO MATRICIAL")
    print("-"*76)
    print("Orden Euler:",best["orden"])
    print("Modo Euler:",best["modo"])
    print("Boresight:",best["boresight_side"])
    print(f"Signos IMU: Yaw={best['sign_yaw']:+d}, Pitch={best['sign_pitch']:+d}, Roll={best['sign_roll']:+d}")
    print(f"Mediana: {best['mediana_deg']:.3f}°")
    print(f"Media:   {best['media_deg']:.3f}°")
    print(f"RMSE:    {best['rmse_deg']:.3f}°")
    print(f"P95:     {best['p95_deg']:.3f}°")
    print(f"Máximo:  {best['max_deg']:.3f}°")
    print("QC:",qc)
    print("\nIMPORTANTE: no generalizar este boresight sin validación inter-sesión.")

if __name__=="__main__":
    main()
