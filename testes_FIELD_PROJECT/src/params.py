# Parâmetros da simulação — ajuste conforme necessário
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

query = {
    'projeto': 'planejamento-animale-292719',
    'data0': '2025-08-16', # Formato AAAA-MM-DD
    'tabela_bigquery': 'planejamento-animale-292719.checklists_rollout.ANIMALE_checklist',
}

params = {
    'alpha': 0.7, # preferência do CD ao ser provedor
    'p': 1.0, # peso para cont_rup
    'q': 0.5, # peso para cont_falta
    'k_cd': 0.02, # custo por km para CD
    'k_filial': 0.04, # custo por km para filial
    'c': 0.05, # fator leadtime = c * distancia
}

paths = {
    'caminho_distancias': os.path.join(BASE_DIR,"../dados/distancias_filiais.csv"),
    'arquivo_filiais': os.path.join(BASE_DIR,"../dados/filiais.json"),
    'cred': os.path.join(BASE_DIR, "../bd/planejamento-animale-292719-296d49ccdea6.json"),
}