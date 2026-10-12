#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validar_sfm_imu_v2_8_5.py

Validación SO(3) usando rotaciones nativas exportadas desde camera.transform.
Explora:
- 4 variantes de orientación SfM;
- 6 órdenes Euler para IMU;
- intrínseco/extrínseco;
- 8 combinaciones de signos;
- 24 cambios de base propios;
- IMU directa/transpuesta;
- boresight izquierda/derecha.

Requiere numpy, pandas y scipy.
"""

from __future__ import annotations
import argparse,itertools,re
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation as R

def normalizar_id(s):
    m=re.search(r"(CAP_\d+)",str(s).upper())
    return m.group(1) if m else str(s).strip().upper()

def matrices_cambio_base():
    mats=[]
    for perm in itertools.permutations(range(3)):
        P=np.eye(3)[:,perm]
        for s in itertools.product([1,-1],repeat=3):
            M=P@np.diag(s)
            if np.linalg.det(M)>0.999:
                mats.append(("perm"+"".join(str(i+1) for i in perm)+"_s"+"".join("+" if x>0 else "-" for x in s),M))
    # 24 rotaciones propias
    return mats

def rot_media(mats): return R.from_matrix(np.asarray(mats)).mean().as_matrix()

def error_deg(A,B):
    rel=np.einsum("nij,njk->nik",np.transpose(A,(0,2,1)),B)
    tr=np.clip((np.trace(rel,axis1=1,axis2=2)-1)/2,-1,1)
    return np.rad2deg(np.arccos(tr))

def imu_euler(df,orden,modo,sig):
    vals={
        "yaw":df["yaw_parrot_deg"].to_numpy()*sig[0],
        "pitch":df["pitch_parrot_deg"].to_numpy()*sig[1],
        "roll":df["roll_parrot_deg"].to_numpy()*sig[2],
    }
    seq="".join({"yaw":"z","pitch":"x","roll":"y"}[k] for k in orden)
    if modo=="intrinsic": seq=seq.upper()
    ang=np.column_stack([vals[k] for k in orden])
    return R.from_euler(seq,ang,degrees=True).as_matrix()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--imu",default="Sequoia_Organizado/Reportes/metashape_axis_mapping_candidates_v282.csv")
    ap.add_argument("--sfm-native",default="Sequoia_Organizado/Reportes/metashape_native_rotations_v284a.csv")
    ap.add_argument("--reportes",default="Sequoia_Organizado/Reportes")
    args=ap.parse_args()

    imu=pd.read_csv(args.imu); sfm=pd.read_csv(args.sfm_native)
    if "master_gre" in sfm.columns:
        sfm=sfm[sfm["master_gre"].astype(int)==1].copy()
    else:
        sfm=sfm[sfm["label"].astype(str).str.contains("_GRE",case=False,regex=False)].copy()
    sfm["capture_id"]=sfm["label"].map(normalizar_id)
    imu["capture_id"]=imu["capture_id"].map(normalizar_id)
    d=sfm.merge(imu,on="capture_id",how="inner")
    if d.empty: raise SystemExit("No hay pares coincidentes.")

    base=np.stack([d[[f"r{i}{j}" for i in range(1,4) for j in range(1,4)]].to_numpy()[k].reshape(3,3) for k in range(len(d))])
    variantes={
        "cam_direct":base,
        "cam_transpose":np.transpose(base,(0,2,1)),
        "cam_neg_z":base@np.diag([1,-1,-1]),
        "cam_neg_z_transpose":np.transpose(base@np.diag([1,-1,-1]),(0,2,1)),
    }

    ordenes=list(itertools.permutations(["yaw","pitch","roll"]))
    modos=["extrinsic","intrinsic"]; signos=list(itertools.product([1,-1],repeat=3))
    frames=matrices_cambio_base()

    modelos=[]; best=None; best_err=None; bestB=None
    for sfm_name,sfmR in variantes.items():
        for orden in ordenes:
            for modo in modos:
                for sig in signos:
                    I=imu_euler(d,orden,modo,sig)
                    for frame_name,C in frames:
                        Ic=np.einsum("ij,njk,kl->nil",C,I,C.T)
                        for transp in [0,1]:
                            J=np.transpose(Ic,(0,2,1)) if transp else Ic
                            for lado in ["left","right"]:
                                if lado=="left":
                                    Bs=np.einsum("nij,njk->nik",sfmR,np.transpose(J,(0,2,1)))
                                    B=rot_media(Bs)
                                    pred=np.einsum("ij,njk->nik",B,J)
                                else:
                                    Bs=np.einsum("nij,njk->nik",np.transpose(J,(0,2,1)),sfmR)
                                    B=rot_media(Bs)
                                    pred=np.einsum("nij,jk->nik",J,B)
                                err=error_deg(pred,sfmR)
                                row={
                                    "sfm_variant":sfm_name,
                                    "imu_order":">".join(orden),
                                    "imu_mode":modo,
                                    "sign_yaw":sig[0],"sign_pitch":sig[1],"sign_roll":sig[2],
                                    "frame":frame_name,
                                    "imu_transpose":transp,
                                    "boresight_side":lado,
                                    "median_deg":float(np.median(err)),
                                    "mean_deg":float(np.mean(err)),
                                    "rmse_deg":float(np.sqrt(np.mean(err**2))),
                                    "p95_deg":float(np.percentile(err,95)),
                                    "max_deg":float(np.max(err)),
                                }
                                modelos.append(row)
                                if best is None or row["median_deg"]<best["median_deg"]:
                                    best=row; best_err=err.copy(); bestB=B.copy()

    rep=Path(args.reportes); rep.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(modelos).sort_values("median_deg").to_csv(rep/"sfm_imu_modelos_v285.csv",index=False)
    pd.DataFrame([best]).to_csv(rep/"sfm_imu_mejor_modelo_v285.csv",index=False)
    rr=d[["capture_id","label"]].copy(); rr["error_angular_deg"]=best_err
    rr.to_csv(rep/"sfm_imu_residuales_v285.csv",index=False)
    np.savetxt(rep/"boresight_matrix_v285.csv",bestB,delimiter=",")

    qc="COHERENCIA_ALTA" if best["median_deg"]<3 else ("COHERENCIA_INTERMEDIA_REVISAR_BORESIGHT" if best["median_deg"]<8 else "COHERENCIA_BAJA_REVISAR_MODELO")
    print("="*76)
    print("VALIDACIÓN NATIVA SfM–IMU v2.8.5")
    print("="*76)
    print("Pares SfM–IMU coincidentes:",len(d))
    print("Modelos probados:",len(modelos))
    print("\nMEJOR MODELO NATIVO")
    print("-"*76)
    print("SfM:",best["sfm_variant"])
    print("IMU order:",best["imu_order"])
    print("IMU mode:",best["imu_mode"])
    print(f"Signos: Yaw={best['sign_yaw']:+d}, Pitch={best['sign_pitch']:+d}, Roll={best['sign_roll']:+d}")
    print("Frame:",best["frame"])
    print("IMU transpose:",best["imu_transpose"])
    print("Boresight side:",best["boresight_side"])
    print(f"Mediana: {best['median_deg']:.3f}°")
    print(f"Media:   {best['mean_deg']:.3f}°")
    print(f"RMSE:    {best['rmse_deg']:.3f}°")
    print(f"P95:     {best['p95_deg']:.3f}°")
    print(f"Máximo:  {best['max_deg']:.3f}°")
    print("QC:",qc)
    print("\nNo generalizar a otras sesiones sin validación inter-sesión.")

if __name__=="__main__":
    main()
