import argparse
import pandas as pd
import numpy as np
from params import params
from bd_utils import construir_bd_inicial, classificar_filiais, atualizar_transitos_para_estoque
from ranking import montar_matriz_T
from transferencia import quantidade_desejada, excesso_disponivel, executar_transferencia
from vendas import simular_venda_poisson, atualizar_alvo

def main(data0, dias, caminho_distancias, caminho_bd_query):
    # carregar arquivos de exemplo
    df_distancias = pd.read_csv(caminho_distancias)
    df_query = pd.read_csv(caminho_bd_query)
    
    df = construir_bd_inicial(df_query)
    
    # envios: guarda envios pendentes e históricos
    envios = pd.DataFrame(columns=['dia_envio','dia_chegada','A','B','SKU','q'])

    historico_envios = []
    snapshots = []
    #leadtime = df_distancias.loc[(df_distancias['Filial_A']==A) & (df_distancias['Filial_B']==B),'LeadTime'].values[0]

    for dia in range(1, dias+1):
        print(f"Rodando dia {dia}")
        # 1) aplicar chegadas de envios programados
        df = atualizar_transitos_para_estoque(df, dia, envios)
        # 2) classificar
        prov, rec = classificar_filiais(df)
        if rec.empty or prov.empty:
            snapshots.append((dia, df.copy()))
            continue
        # 3) montar matriz
        T = montar_matriz_T(prov, rec, df_distancias, params)
        # 4) alocar: para cada B, achar A max
        for B in T.columns:
            A = T[B].idxmax()
            if pd.isna(A):
                continue
            # iterar por SKUs que B precisa
            skus = df[df['FILIAL']==B]['SKU'].unique().tolist()
            for sku in skus:
                desejo = quantidade_desejada(df, B, sku)
                if desejo <= 0:
                    continue
                disponivel = excesso_disponivel(df, A, sku)
                if disponivel <= 0:
                    continue
                q = min(desejo, disponivel)
                q, envios = executar_transferencia(df, A, B, sku, q, dia_envio=dia, dias_transito=params.get('dia_transito_default',2),envios_df=envios)
                historico_envios.append({'dia':dia,'A':A,'B':B,'SKU':sku,'q':q})
                # se A ficou sem excesso, remover da lista de provedores (simples: atualizar prov e T)
                if excesso_disponivel(df, A, sku) <= 0:
                    # marcar linha A inteira como 0 em T
                    if A in T.index:
                        T.loc[A,:] = 0
        # 5) simular VENDAS (reduz EST_DISP)
        for idx,row in df.iterrows():
            venda = simular_venda_poisson(row.get('VELOCIDADE_VENDA',0),row.get('EST_DISP',0))
            df.at[idx,'EST_DISP'] = max(0, df.at[idx,'EST_DISP'] - venda)
        # 6) atualizar alvo simples
        #df = atualizar_alvo(df, leadtime_por_filial)
        # snapshot do dia
        snapshots.append((dia, df.copy()))

    # salvar outputs
    pd.DataFrame(historico_envios).to_csv('outputs/envios.csv', index=False)
    # snapshots: salvar o ultimo
    snapshots[-1][1].to_csv('outputs/estoque_final.csv', index=False)
    print('Simulação finalizada. Outputs em outputs/')
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data0', required=True)
    parser.add_argument('--dias', type=int, default=30)
    parser.add_argument('--dist', default='exemplos/distancias_todas_combinacoes.csv')
    parser.add_argument('--bd', default='exemplos/simulacao_diaria.csv')
    args = parser.parse_args()
    main(args.data0, args.dias, args.dist, args.bd)
