# pi_tec_BD_supermercado
Projeto Integrador de Ciência de Dados aplicado à análise de vendas de supermercado.

**[Acesse o Dashboard Interativo no Streamlit](https://pitecbdsupermercado-rx7gpvlsw9gk3mw6fxvgmv.streamlit.app)**

---

##  1ª Entrega: Análise Exploratória e Visualizações

A partir da base de dados escolhida, foram propostas inicialmente cinco visualizações orientadas à tomada de decisões:

### 1. Faturamento por categoria de produto

- **Visualização:** Comparação do faturamento entre as categorias de produtos.
- **Decisão apoiada:** Identificar quais categorias merecem maior prioridade de estoque, espaço na loja ou investimento.

### 2. Faturamento por filial ou cidade

- **Visualização:** Comparação do desempenho das diferentes unidades.
- **Decisão apoiada:** Identificar filiais com melhor ou pior desempenho e direcionar investimentos ou ações corretivas.

### 3. Quantidade de transações por horário

- **Visualização:** Comparação da quantidade de transações realizadas em cada horário.
- **Decisão apoiada:** Auxiliar no planejamento da escala de funcionários, da reposição de produtos e de promoções para horários com menor movimento.

### 4. Formas de pagamento utilizadas

- **Visualização:** Comparação da utilização de dinheiro, cartão e carteira digital.
- **Decisão apoiada:** Adaptar os meios de pagamento oferecidos e planejar promoções direcionadas.

### 5. Avaliação média por categoria de produto

- **Visualização:** Comparação da avaliação média atribuída pelos clientes a cada categoria.
- **Decisão apoiada:** Identificar categorias com avaliações inferiores e orientar investigações sobre qualidade, variedade, preço ou experiência de compra.

> As análises foram desenvolvidas com Pandas e NumPy, e as cinco visualizações foram produzidas com Matplotlib.

---

## 2ª Entrega: Engenharia de Dados, Data Warehouse e Dashboard (BI)

Na segunda etapa do projeto, a solução evoluiu para uma arquitetura analítica estruturada em banco de dados relacional e disponibilizada em uma aplicação web interativa:

### 1. Arquitetura e Especificação dos Recursos do SGBD (`supermercado_dw`)
- **SGBD e Armazenamento:** Implementação em **MySQL 8.0** utilizando o motor transacional `InnoDB` (conformidade ACID e integridade referencial) e codificação `utf8mb4`.
- **Modelagem Dimensional (Star Schema):** Estruturação da tabela fato `fato_vendas` conectada a cinco dimensões (`ttempo`, `tfilial`, `tproduto`, `tcliente` e `tpagamento`), além da tabela operacional `etl_auditoria` para rastreabilidade das cargas.
- **Integridade, Segurança e Performance:** Aplicação de restrições declarativas (`PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`, `CHECK`, `ENUM`), controle de acesso baseado em papéis (`role_dba`, `role_etl`, `role_bi_streamlit`), índices `B-Tree` para otimização de consultas analíticas e **Views OLAP** pré-agregadas.

### 2. Script de Construção do Banco (`dump_supermarket_dw`)
- Disponibilização do arquivo de *dump* SQL contendo toda a estrutura DDL (tabelas, restrições, índices, papéis/permissões e views analíticas) e a carga de dados (DML) para replicação completa do Data Warehouse.

### 3. Implantação de Algoritmo de Aprendizado de Márquinas para Análise de Agrupamento

- Aplicação do algoritmo: Utilização do algoritmo de aprendizado não supervisionado K-Means para agrupar transações com características semelhantes, considerando variáveis como valor da compra, quantidade de itens e avaliação do cliente.

Objetivo: Identificar padrões de comportamento nas compras e segmentar as transações em grupos (clusters), permitindo explorar diferenças entre os perfis de consumo e apoiar análises estratégicas do negócio.

### 4. Aplicação Analítica Interativa (`app.py`)
- Desenvolvimento de um painel gerencial interativo em **Python** com **Streamlit**, conectado às *Views* do Data Warehouse para suportar operações analíticas multidimensionais (*Slice*, *Dice*, *Drill-Down* e *Roll-Up*), monitoramento de KPIs executivos e análise de agrupamento de transações (*K-Means*).
- **Acesso online:** [https://pitecbdsupermercado-rx7gpvlsw9gk3mw6fxvgmv.streamlit.app](https://pitecbdsupermercado-rx7gpvlsw9gk3mw6fxvgmv.streamlit.app)

---

### Integrantes
> DANIEL FELIPE SOUZA DA SILVA<br>
> JONATHAN MUSSATO SILVA<br>
> LUCAS PEREIRA STEFANINI<br>
