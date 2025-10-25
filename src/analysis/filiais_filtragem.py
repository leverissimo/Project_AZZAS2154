import os
import json
import pandas as pd
from utils.gcp_connection import query_to_df

# === QUERY PRINCIPAL ===
QUERY_FILIAIS = """
WITH base AS (
    SELECT FILIAL, DATA, COUNTIF(RESSUPRIR <> 0) AS produtos_com_ressuprimento
    FROM `planejamento-animale-292719.checklists_rollout.ANIMALE_checklist`
    WHERE DATA > '2025-01-15' AND DATA < '2025-10-06'
    GROUP BY FILIAL, DATA
),
status_filial AS (
    SELECT FILIAL, DATA,
           CASE WHEN produtos_com_ressuprimento = 0 THEN 1 ELSE 0 END AS sem_ressuprimento
    FROM base
),
marcacao_inicio AS (
    SELECT FILIAL, DATA, sem_ressuprimento,
           CAST(
               CASE
                   WHEN sem_ressuprimento = 1
                    AND LAG(sem_ressuprimento, 1, 0) OVER (PARTITION BY FILIAL ORDER BY DATA) = 0
                   THEN 1 ELSE 0
               END AS INT64
           ) AS inicio_periodo
    FROM status_filial
),
grupos AS (
    SELECT FILIAL, DATA, sem_ressuprimento,
           SUM(inicio_periodo) OVER (
               PARTITION BY FILIAL ORDER BY DATA ROWS UNBOUNDED PRECEDING
           ) AS periodo_id
    FROM marcacao_inicio
    WHERE sem_ressuprimento = 1
),
resumo AS (
    SELECT FILIAL, periodo_id AS ID_PERIODO,
           MIN(CAST(DATA AS DATE)) AS inicio_sem_ressuprimento,
           MAX(CAST(DATA AS DATE)) AS fim_sem_ressuprimento,
           DATE_DIFF(MAX(CAST(DATA AS DATE)), MIN(CAST(DATA AS DATE)), DAY) + 1 AS dias_sem_ressuprimento
    FROM grupos
    GROUP BY FILIAL, periodo_id
),
classificado AS (
    SELECT r.*,
           CASE 
               WHEN r.fim_sem_ressuprimento = (
                   SELECT MAX(CAST(DATA AS DATE)) FROM status_filial s WHERE s.FILIAL = r.FILIAL
               ) THEN 'EM ANDAMENTO'
               ELSE 'FINALIZADO'
           END AS STATUS,
           CASE 
               WHEN r.dias_sem_ressuprimento > 30 THEN 'SUPERIOR A 30 DIAS'
               ELSE 'ATE 30 DIAS'
           END AS CLASSIFICACAO
    FROM resumo r
),
agrupado AS (
    SELECT FILIAL,
           MAX(CASE WHEN CLASSIFICACAO = 'SUPERIOR A 30 DIAS' THEN 1 ELSE 0 END) AS teve_periodo_maior_30
    FROM classificado
    GROUP BY FILIAL
)
SELECT a.FILIAL,
       CASE WHEN a.teve_periodo_maior_30 = 1 THEN 'FILIAL COM PERÍODO > 30 DIAS'
            ELSE 'FILIAL SEM PERÍODO > 30 DIAS' END AS STATUS_FILIAL,
       c.ID_PERIODO, c.inicio_sem_ressuprimento, c.fim_sem_ressuprimento,
       c.dias_sem_ressuprimento, c.CLASSIFICACAO, c.STATUS
FROM agrupado a
LEFT JOIN classificado c ON a.FILIAL = c.FILIAL
ORDER BY a.FILIAL, c.ID_PERIODO;
"""

def main():
    print("Executando análise de filiais...")
    df = query_to_df(QUERY_FILIAIS)

    # salva em Excel
    os.makedirs("data", exist_ok=True)
    output_path = os.path.join("data", "ressuprimento_filiais.xlsx")
    df.to_excel(output_path, index=False)
    print(f"Arquivo salvo em {output_path}")

if __name__ == "__main__":
    main()