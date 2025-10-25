import os
from utils.gcp_connection import query_to_df

def main():
    query = """
    SELECT FILIAL, SKU, DATA, RESSUPRIR, ALVO
    FROM `planejamento-animale-292719.checklists_rollout.ANIMALE_checklist`
    WHERE DATA > '2025-01-15' AND DATA < '2025-10-06'
    AND FILIAL LIKE 'ANIMALE MARINGA CM'
    ORDER BY DATA;
    """

    df = query_to_df(query)
    df.to_excel("data/rupturas_maringa.xlsx", index=False)
    print("Arquivo gerado: data/rupturas_maringa.xlsx")

if __name__ == "__main__":
    main()