import sys
import json
import pandas as pd
import params 
from pathlib import Path
PROJECT_ROOT = Path.cwd().resolve().parent
sys.path.append(str(PROJECT_ROOT))
from gcpUtils import auth 
from gcpUtils import bigQuery as bQ

def query():
    
    arquivoFiliais = params.paths['arquivo_filiais']
    cred = auth.getCredentials(params.paths['cred'])
    tabela_bigquery = params.query['tabela_bigquery']
    data0 = params.query['data0']

    with open(arquivoFiliais, 'r', encoding='utf-8') as f:
        dados_filiais = json.load(f)
        
    df_filiais = pd.DataFrame(dados_filiais)

    lista_nomes_filiais = df_filiais['FILIAL'].unique().tolist()

    filiaisQuery = f"('{ "','".join(lista_nomes_filiais)}')"

    query = f"""
        SELECT SKU, FILIAL, DATA, VELOCIDADE_VENDA, ALVO, TRANSITO, EST_DISP, EST_TOTAL, VOLUME_EXCESSO, VOLUME_FALTA, REGULADOR
        FROM {tabela_bigquery}
        WHERE FILIAL IN {filiaisQuery}
        AND DATA = '{data0}'
    """
    df_query = bQ.tableToPandas(query,params.query['projeto'], cred)
    return df_query

#query().to_csv('teste_query.csv', index=False)


