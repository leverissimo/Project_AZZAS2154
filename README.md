# Project_AZZAS2154
# DESAFIO: Indicadores de Performance e Eficiência da Distribuição  

Este projeto foi desenvolvido no contexto do **Fields**, programa de integração entre empresas e alunos da **EMAp/FGV**, em parceria com a empresa **AZZAS**.  
O desafio proposto consistiu em **analisar e propor indicadores para medir a performance e a eficiência do processo de distribuição de peças entre filiais e centros de distribuição (CDs)**.

## Equipe

- **Samyra Mara** 
- **Leonardo Veríssimo** 
- **Gabrielly Chácara**  

## Objetivo do Projeto

Desenvolver um sistema analítico capaz de:

- Identificar **rupturas de estoque** e **excessos** nas filiais;  
- Avaliar o **lead time**, **tempo de transporte** e **custos de envio** entre lojas e CDs;  
- Simular **estratégias de redistribuição entre filiais**, considerando custo e tempo otimizados;  
- Criar **indicadores confiáveis de eficiência** e validar sua eficácia antes e depois da aplicação das regras propostas.


## Estrutura do Projeto

# 🧱 Estrutura Final do Projeto

```arduino
Project_AZZAS2154/
│
├── src/
│   ├── __init__.py
│   │
│   ├── analysis/               # scripts analíticos
│   │   ├── filiais.py
│   │   ├── filiais_filtragem.py
│   │   ├── geral.py
│   │   └── produtos.py
│   │
│   ├── etl/                    # pipeline de criação de mapas
│   │   └── criacao_de_mapa.py
│   │
│   ├── gcpUtils/               # integração com Google Cloud
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── bigQuery.py
│   │   ├── cloudStorage.py
│   │   ├── google_storage_manager.py
│   │   ├── osUtils.py
│   │   ├── visionApi.py
│   │   ├── requirements.txt
│   │   └── README.md
│   │
│   └── utils/                  # utilitários locais
│       ├── config.py
│       ├── gcp_connection.py
│       └── io_helpers.py
│
├── data/
│   ├── raw/                    # dados brutos
│   │   ├── json/               # mover conteúdo de ./dados/
│   │   │   ├── filiais_UF_SP.json
│   │   │   ├── filiais_inferior_30.json
│   │   │   ├── pesquisa_estatisticas.json
│   │   │   └── todas_filiais.json
│   │   │
│   │   └── excel/              # mover conteúdo de ./data/
│   │       ├── ressuprimento_filiais.xlsx
│   │       ├── rupturas_anuale_checklist.xlsx
│   │       ├── rupturas_avaliadas_checklist.xlsx
│   │       ├── rupturas_avaliadas_iet_checklist.xlsx
│   │       └── rupturas_buzios.xlsx
│   │
│   └── processed/              # resultados intermediários
│
├── resultados/                 # saídas finais
│   ├── csvs/
│   ├── graficos/
│   └── mapas_gerados/
│
├── mapas_de_filiais/           # mapas HTML/JSON gerados
│   ├── mapa_filiais.html
│   ├── RJ/
│   │   ├── filiais_UF_RJ.json
│   │   └── mapa_filiais_RJ.html
│   └── SP/
│       ├── filiais_UF_SP.json
│       └── mapa_filiais_SP.html
│
├── notebooks/                  # notebooks Jupyter de análise
│   ├── analise.ipynb
│   ├── analise_filiais.ipynb
│   ├── analise_filiais_filtragem.ipynb
│   ├── analise_produtos.ipynb
│   ├── criacao_de_mapa.ipynb
│   ├── hipotese1.ipynb
│   └── visualizacao.ipynb
│
├── simulacao/                  
│   ├── dados_simulacao/
│   │   └── todas_sem_CD.json
│   └── simulacao_inicial.ipynb
│
├── bd/                         # credenciais de acesso GCP
│   ├── W_FILIAIS_202508281436.json
│   ├── bquxjob_5587f672_198f2714903.json
│   └── planejamento-animale-292719-296d49ccdea6.json
│
└── README.md                  
´´´
