import pandas as pd
import query
CD = 'CENTRO DE DISTRIBUICAO'

def construir_bd_inicial():
    """Retorna df pronto para simulação, com CD adicionado e correcoes.
    """
    df_query = query.query()
    df = df_query.copy()
    
    df['TRANSITO'] = 0                         # Zerar trânsito
    df['EST_DISP'] = df['EST_TOTAL']           # Estoque disp = total
    
    df['CONT_RUPTURA_DISP'] = (df.apply(categorizar_estDisp, axis=1) == 'RUPTURA').astype(int)
    df['CONT_FALTA_DISP']   = (df.apply(categorizar_estDisp, axis=1) == 'FALTA').astype(int)
    df['CONT_EXCESSO_DISP'] = (df.apply(categorizar_estDisp, axis=1) == 'EXCESSO').astype(int)
    
    df['CONT_RUPTURA'] = (df.apply(categorizar_estTotal, axis=1) == 'RUPTURA').astype(int)
    df['CONT_FALTA']   = (df.apply(categorizar_estTotal, axis=1) == 'FALTA').astype(int)
    df['CONT_EXCESSO'] = (df.apply(categorizar_estTotal, axis=1) == 'EXCESSO').astype(int)
    
    # construir CD: somar REGULADOR por SKU
    df_cd = df.groupby(['SKU', 'DATA'], as_index=False)['REGULADOR'].sum()
    df_cd = df_cd.rename(columns={'REGULADOR': 'EST_TOTAL'})
    df_cd['FILIAL'] = CD
    df_cd['EST_DISP'] = df_cd['EST_TOTAL']
    df_cd['VOLUME_EXCESSO'] = df_cd['EST_TOTAL']
    df_cd['CONT_EXCESSO'] = (df_cd['EST_TOTAL'] > 0).astype(int)
    df_cd['CONT_RUPTURA'] = (df_cd['EST_TOTAL'] == 0).astype(int)
    df_cd['CONT_EXCESSO_DISP'] = df_cd['CONT_EXCESSO']
    df_cd['CONT_RUPTURA_DISP'] = df_cd['CONT_RUPTURA']
   
    # preenchimentos mínimos de colunas esperadas
    for c in ['VELOCIDADE_VENDA','ALVO','VOLUME_FALTA','TRANSITO','CONT_FALTA', 'CONT_FALTA_DISP']:
        if c not in df_cd.columns:
            df_cd[c] = 0
            
    
    # remover coluna REGULADOR do df original
    df = df.drop(columns=["REGULADOR"], errors='ignore')
            
    # juntar
    df_final = pd.concat([df, df_cd], ignore_index=True, sort=False)
    
    # garantir tipos e NaNs
    df_final = df_final.fillna(0)
    return df_final

def categorizar_estTotal(row):
    est = row['EST_TOTAL']
    alvo = row['ALVO']

    if est == 0:
        return 'RUPTURA'
    if est < alvo:
        return 'FALTA'
    if est > alvo:
        return 'EXCESSO'
    return 'OK'

def categorizar_estDisp(row):
    est = row['EST_DISP']
    alvo = row['ALVO']

    if est == 0:
        return 'RUPTURA'
    if est < alvo:
        return 'FALTA'
    if est > alvo:
        return 'EXCESSO'
    return 'OK'

def classificar_filiais(df):
    df_prov = df[df['CONT_EXCESSO_DISP'] == 1].copy()
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

construir_bd_inicial().to_csv('teste_bd_inicial.csv', index=False)