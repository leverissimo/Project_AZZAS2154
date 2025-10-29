import os
from gcpUtils.auth import getCredentials
from gcpUtils.bigQuery import pandasToBq, tableToPandas

def get_cred():
    """Retorna as credenciais padrão do projeto GCP."""
    cred_path = os.path.join("..", "bd", "planejamento-animale-292719-296d49ccdea6.json")
    return getCredentials(cred_path)

def query_to_df(query: str, project: str = "planejamento-animale-292719"):
    """Executa uma query no BigQuery e retorna um DataFrame."""
    cred = get_cred()
    df = tableToPandas(query, project, cred)
    df.columns = df.columns.str.upper()
    return df