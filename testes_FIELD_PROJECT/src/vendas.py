import numpy as np

def simular_venda_poisson(vel14, est_disp):
    """vel14: velocidade de venda (quantidade esperada nos ultimos 14 dias).
    Para dia, aproximamos lambda = vel14 / 14.
    """
    if vel14 <= 0:
        return 0
    lam = vel14 / 14.0
    demanda = np.random.poisson(lam)
    venda = int(min(demanda, est_disp))
    return venda

def atualizar_velocidade(df, historico_vendas, dia_atual, janela=14):
    """
    Recalcula VELOCIDADE_VENDA para cada linha do df a partir da soma
    das vendas nos últimos `janela` dias (inclui dia_atual-1 até dia_atual-janela).
    - df: DataFrame atual com colunas ['FILIAL','SKU', ...]. A coluna VELOCIDADE_VENDA será atualizada.
    - historico_vendas: DataFrame com colunas ['dia','FILIAL','SKU','venda'] (dia é int ou datetime index coerente).
    - dia_atual: int (ou compatível) que marca o dia da simulação (por ex. 1,2,...).
    - janela: número de dias (14 por padrão).
    Retorna df (mutado) e, opcionalmente, um DataFrame com velocidades por par (para debug).
    """
    # limite inferior (exclui o próprio dia atual se você quiser usar só até ontem): [dia_atual-janela, dia_atual-1]
    inicio = dia_atual - janela
    fim = dia_atual - 1

    # otimização: agrupa histórico apenas uma vez
    mask = (historico_vendas['dia'] >= inicio) & (historico_vendas['dia'] <= fim)
    hist_window = historico_vendas.loc[mask]

    # soma por par (FILIAL, SKU)
    agreg = hist_window.groupby(['FILIAL','SKU'], as_index=False)['venda'].sum()
    agreg = agreg.rename(columns={'venda':'vel_ultimos_'+str(janela)+'d'})

    # juntar com df
    df = df.merge(agreg, how='left', left_on=['FILIAL','SKU'], right_on=['FILIAL','SKU'])
    df['vel_ultimos_'+str(janela)+'d'] = df['vel_ultimos_'+str(janela)+'d'].fillna(0)

    # VELOCIDADE_VENDA: manter a mesma definição que você usa na base (soma nos ultimos 14 dias)
    df['VELOCIDADE_VENDA'] = df['vel_ultimos_'+str(janela)+'d']

    # remover coluna auxiliar
    df = df.drop(columns=['vel_ultimos_'+str(janela)+'d'])

    return df

def atualizar_alvo(df, leadtime_por_filial):
# Exemplo simples: ALVO = ceil(VELOCIDADE_VENDA * LEADTIME_FILIAL)
    for idx,row in df.iterrows():
        lt = leadtime_por_filial.get(row['FILIAL'], 1)
        df.at[idx,'ALVO'] = int(np.ceil(row.get('VELOCIDADE_VENDA',0) * lt))
    return df
