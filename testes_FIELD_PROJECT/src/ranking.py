import numpy as np
import pandas as pd
from params import params

CD = 'CENTRO DE DISTRIBUICAO'

def get_distancia(a, b, dist_df):
    if a == b:
        return 0
    cond = ((dist_df['Filial_A'] == a) & (dist_df['Filial_B'] == b)) | ((dist_df['Filial_A'] == b) & (dist_df['Filial_B'] == a))
    row = dist_df[cond]
    if row.empty:
        return np.inf
    return row['Distancia_km'].values[0]

def calcular_ranking_F(provedor, receptor, dist_df, params_local, cont_rup, cont_falta):
    dist = get_distancia(provedor, receptor, dist_df)
    if not np.isfinite(dist) or dist == 0:
        return 0.0
    
    leadtime = params_local['c'] * dist
    if provedor == CD:
        custo_frete = params_local['k_cd'] * dist
    else:
        custo_frete = params_local['k_filial'] * dist
    
    f_ab = ((1.0 / (leadtime + 1.0)) + (1.0 / (custo_frete + 1.0))) * ((cont_rup * params_local['p']) + (cont_falta * params_local['q']))
    if provedor == CD:
        return params_local['alpha'] * f_ab
    return f_ab

def montar_matriz_T(df_prov, df_rec, dist_df, params_local):
    provedores = df_prov['FILIAL'].unique().tolist()
    receptoras = df_rec['FILIAL'].unique().tolist()

    T = pd.DataFrame(index=provedores, columns=receptoras, data=0.0)
    for B in receptoras:
        # identificar status B: 
        row = df_rec[df_rec['FILIAL'] == B].iloc[0]
        cont_rup = 1 if row['CONT_RUPTURA'] == 1 else 0
        cont_falta = 1 if row['CONT_FALTA'] == 1 else 0
        
        for A in provedores:
            T.loc[A, B] = calcular_ranking_F(A, B, dist_df, params_local, cont_rup, cont_falta)
    
    return T