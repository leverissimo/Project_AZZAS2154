import pandas as pd

def quantidade_desejada(df, B, SKU):
    mask = (df['FILIAL'] == B) & (df['SKU'] == SKU)
    if mask.sum() == 0:
        return 0
    alvo = df.loc[mask, 'ALVO'].iloc[0]
    est_disp = df.loc[mask, 'EST_DISP'].iloc[0]
    return max(0, alvo - est_disp)

def excesso_disponivel(df, A, SKU):
    mask = (df['FILIAL'] == A) & (df['SKU'] == SKU)
    if mask.sum() == 0:
        return 0
    
    est_disp = df.loc[mask, 'EST_DISP'].iloc[0]
    # excesso medido sobre ALVO: quanto além do alvo A pode doar
    alvo = df.loc[mask, 'ALVO'].iloc[0] if 'ALVO' in df.columns else 0
    return max(0, est_disp - alvo)


def executar_transferencia(df, A, B, SKU, q, dia_envio, dias_transito, envios_df):
    # q: quantidade a transferir
    # atualiza df e registra no envios_df (pandas DataFrame)
    maskA = (df['FILIAL'] == A) & (df['SKU'] == SKU)
    maskB = (df['FILIAL'] == B) & (df['SKU'] == SKU)

    if maskA.sum() == 0 or maskB.sum() == 0:
        return 0

    q = min(q, df.loc[maskA, 'EST_DISP'].iloc[0])
    if q <= 0:
        return 0

    df.loc[maskA, 'EST_DISP'] -= q
    df.loc[maskB, 'TRANSITO'] += q

    dia_chegada = dia_envio + dias_transito
    envios_df = envios_df.append({
        'dia_envio': dia_envio,
        'dia_chegada': dia_chegada,
        'A': A,
        'B': B,
        'SKU': SKU,
        'q': q
    }, ignore_index=True)
    
    return q, envios_df