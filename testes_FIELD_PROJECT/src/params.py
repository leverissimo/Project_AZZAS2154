# Parâmetros da simulação — ajuste conforme necessário
params = {
    'alpha': 0.7, # preferência do CD ao ser provedor
    'p': 1.0, # peso para cont_rup
    'q': 0.6, # peso para cont_falta
    'k_cd': 0.02, # custo por km para CD
    'k_filial': 0.04, # custo por km para filial
    'c': 0.05, # fator leadtime = c * distancia
    'dia_transito_default': 2, # dias padrão até o envio chegar
}