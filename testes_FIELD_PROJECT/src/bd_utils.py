import pandas as pd
CD = 'CENTRO DE DISTRIBUICAO'

def construir_bd_inicial(df_query):
    """Recebe o df retornado da query.
    Retorna df pronto para simulação, com CD adicionado e correcoes.
    """
    df = df_query.copy()
    
    # incorporando embalado e reservado ao estoque total e ao transito
    for col in ['EMBALADO','RESERVADO']:
        if col in df.columns:
            df['EST_TOTAL'] = df['EST_TOTAL'].fillna(0) + df[col].fillna(0)
            df['TRANSITO'] = df['TRANSITO'].fillna(0) + df[col].fillna(0)
    # drop col extras
    for col in ['EMBALADO','RESERVADO']:
        if col in df.columns:
            df = df.drop(columns=[col])
    # construir CD: somar REGULADOR por SKU
    if 'REGULADOR' in df.columns:
        df_cd = df.groupby('SKU', as_index=False)['REGULADOR'].sum()
        df_cd = df_cd.rename(columns={'REGULADOR': 'EST_TOTAL'})
    else:
        df_cd = pd.DataFrame(columns=['SKU','EST_TOTAL'])
    if not df_cd.empty:
        df_cd['FILIAL'] = CD
        df_cd['EST_DISP'] = df_cd['EST_TOTAL']
        df_cd['TRANSITO'] = 0
        # preenchimentos mínimos de colunas esperadas
        for c in ['VELOCIDADE_VENDA','ALVO','CONT_RUPTURA','CONT_FALTA','CONT_EXCESSO','VOLUME_EXCESSO','VOLUME_FALTA']:
            if c not in df_cd.columns:
                df_cd[c] = 0
    # juntar
        df_final = pd.concat([df, df_cd], ignore_index=True, sort=False)
    else:
        df_final = df
        
    # garantir tipos e NaNs
    df_final = df_final.fillna(0)
    return df_final

def classificar_filiais(df):
    df_prov = df[df['CONT_EXCESSO'] == 1].copy()
    df_rec = df[(df['CONT_RUPTURA'] == 1) | (df['CONT_FALTA'] == 1)].copy()
    return df_prov, df_rec

def atualizar_transitos_para_estoque(df, dia_atual, envios_df):
    """Atualiza o EST_DISP a partir de envios cuja data prevista de chegada é
    hoje."""
    # envios_df deve conter: dia_envio, dia_chegada, A, B, SKU, q
    chegadas = envios_df[envios_df['dia_chegada'] == dia_atual]
    for _, row in chegadas.iterrows():
        mask = (df['FILIAL'] == row['B']) & (df['SKU'] == row['SKU'])
        df.loc[mask, 'TRANSITO'] = df.loc[mask, 'TRANSITO'] - row['q']
        df.loc[mask, 'EST_DISP'] = df.loc[mask, 'EST_DISP'] + row['q']
    return df