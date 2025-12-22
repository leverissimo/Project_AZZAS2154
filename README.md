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

## Principais arquivos e localizações (prioridade máxima)

As partes mais relevantes e de leitura obrigatória para reproduzir a análise e os resultados encontram-se em dois notebooks Jupyter:

* simulacao/simulacao.ipynb — principal notebook de simulação:
    - Contém a simulação de redistribuição, lógica do simulador, parâmetros de entrada e geração dos resultados finais.

    - Este é o ponto de partida para reproduzir as simulações e analisar os outputs agregados por SKU/filial.

    - Recomenda-se abrir esse notebook primeiro e executar as células na ordem apresentada (kernel Python, ambiente com dependências instaladas).

* notebooks/calculo_dias_ruptura.ipynb — cálculo de dias de ruptura:

    - Implementa a metodologia para calcular dias até ruptura, regras de tratamento de dados e validações estatísticas.

    - Serve de suporte ao simulador, fornecendo métricas de entrada e validação das políticas aplicadas.

## Visão geral do repositório

Estrutura resumida (itens relevantes):

- simulacao/
    - simulacao.ipynb <- notebook principal de simulação
    - simulacao_inicial.ipynb
    - simulacoes_skus/, simulacoes_skus_mean/
    - dados_simulacao/
    - comparativo_final.png (exemplo de saída)

- notebooks/
    - calculo_dias_ruptura.ipynb <- notebook de cálculo crítico
    - outros notebooks analíticos (ex.: analise_filiais.ipynb, analise_produtos.ipynb, visualizacao.ipynb)

- src/
    - código utilitário e módulos (ex.: analysis/, gcpUtils/, simular_bd/, criação_de_mapa.py)

- bd/, dados/, mapas_de_filiais/
    - diretórios com dados brutos, arquivos JSON e planilhas utilizadas na análise
- data/
    - criado via execução para armazenar alguns resultados
- notebooks/ e rascunhos/
    - material complementar e rascunhos de análise