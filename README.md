# Modern Beauty – Projeto de Análise de Dados (Portfólio Profissional)
Este projeto implementa um pipeline estruturado de tratamento e integração de dados, partindo de múltiplos arquivos CSV até a geração de datasets consolidados para análise.

A empresa Modern Beauty e os dados utilizados são fictícios e foram criados exclusivamente para fins de portfólio.

O pipeline foi desenvolvido em Python, estruturado de forma modular e executa as seguintes etapas:
- Carregamento dos dados brutos
- Checagem estrutural (validação de colunas esperadas)
- Limpeza e padronização
- Validação de dados (tipos e regras de negócio)
- Integração entre tabelas
- Criação de métricas de negócio
- Geração de datasets finais prontos para análise

## Etapas do Pipeline de Dados
O pipeline foi estruturado nas seguintes etapas modulares:  
<pre> Raw → Data Loader → Check Structure → Data Cleaning → Data Validation → Data Merging → Data Modeling → Processed <pre>

## Objetivo do Projeto
Demonstrar, de forma prática e estruturada, como um Analista de Dados atua desde o dado bruto até a geração de valor para o negócio.
Este projeto simula um fluxo real de trabalho, incluindo:
- Problemas de qualidade de dados
- Integrações entre áreas (Vendas, Marketing, Custos, Clientes)
- Construção de métricas executivas

**O desafio consiste em:**
1. Organizar os dados brutos
2. Corrigir inconsistências
3. Integrar as tabelas corretamente
4. Calcular métricas estratégicas
5. Gerar datasets prontos para análise em BI

## Estrutura do Projeto
<pre>
Modern_beauty/
│
├── data/
│   ├── processed/
│   │   ├── modern_beauty_clientes_campanhas.csv
│   │   └── modern_beauty_vendas.csv
│   │
│   └── raw/
│       ├── campanhas_marketing.csv
│       ├── clientes_atualizado.csv
│       ├── custos.csv
│       ├── produtos.csv
│       └── vendas.csv
│
├── schemas/
│   └── schemas.py
│
├── scripts/
│   ├── __init__.py
│   ├── data_cleaning.py
│   ├── data_loader.py
│   ├── data_merging.py
│   └── data_modeling.py
│
├── tests/
│   ├── test_cleaning.py
│   ├── test_integrity.py
│   ├── test_loader.py
│   ├── test_modeling.py
│   └── test_schemas.py
│
├── validators/
│   └── validators.py
│
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
</pre>

## Stack Utilizada
- Python
- Pandas
- Manipulação de arquivos CSV
- Estrutura modular baseada em scripts
- Pytest (testes automatizados)
- Pydantic (validação de dados e schemas)
- Logging (monitoramento do pipeline)

## Arquitetura do Pipeline de Dados
O pipeline foi estruturado em 7 etapas principais, seguindo boas práticas de engenharia e análise de dados.

**1. Data Loader – Carregamento de Dados**  
Arquivo: data_loader.py  
Os arquivos são carregados a partir do diretório data/raw/

Arquivos utilizados:
- vendas.csv
- produtos.csv
- custos.csv
- clientes_atualizado.csv
- campanhas_marketing.csv

O carregamento é feito via função genérica load_csv(), que:
- Tenta ler o arquivo com pandas.read_csv
- Retorna None caso o arquivo não seja encontrado

No main.py, há uma verificação que interrompe o pipeline caso algum DataFrame não seja carregado corretamente.

**2. Check Structure – Validação de Estrutura**  
Antes da limpeza, o pipeline verifica se os dados possuem todas as colunas esperadas definidas nos schemas.

- Validação baseada em schemas Pydantic
- Interrompe o pipeline caso colunas obrigatórias estejam ausentes
- Emite warnings para colunas extras

**3. Data Cleaning – Limpeza e Padronização de Dados**  
Arquivo: data_cleaning.py  
Esta etapa trata inconsistências comuns em ambientes reais:

**Vendas**
- Padronização de id_produto (ex: P001 → P0001)
- Remoção de espaços
- Conversão da coluna data_venda para datetime
- Remoção de registros com data inválida
- Padronização de forma_pagamento para letras maiúsculas

**Produtos**
- Remoção de espaços em id_produto
- Padronização de nome_produto (Title Case)
- Padronização de categoria
- Ajustes específicos na coluna marca
- Conversão de volume_ml para numérico

**Custos**
- Padronização da coluna fornecedor
- Tratamento de variações de nome

**Clientes**
- Padronização de nome_cliente
- Limpeza de email
- Conversão de data_nascimento e data_cadastro para datetime
- Padronização da coluna sexo (F → Feminino, M → Masculino)
- Padronização de fonte_aquisicao
- Correção de nomes de cidades (ex: POA → Porto Alegre)

**Campanhas**
- Remoção de espaços extras nas colunas canal e ref
- Conversão de data_inicio e data_fim

**4. Data Validation – Validação de Dados**  
Arquivo: validators.py + schemas.py  
Após a limpeza, os dados passam por validação rigorosa utilizando Pydantic:

- Validação de tipos (str, float, datetime, etc.)
- Regras de negócio (ex: valores > 0)
- Tratamento de valores nulos (Optional)

Linhas inválidas:
- São removidas do dataset final
- São registradas em: data/errors/validation_errors.csv

Essa etapa garante alta confiabilidade dos dados antes das integrações.

**5. Data Merging – Integração dos Dados**  
Arquivo: data_merging.py  
Os merges são realizados utilizando pandas.merge() com how="left".

**Relacionamentos aplicados:**  
Vendas + Produtos → id_produto  
Vendas + Custos → id_produto  
Vendas + Clientes → id_cliente  
Clientes + Campanhas → fonte_aquisicao = canal

**Tratamento de valores nulos na relação Clientes + Campanhas:**  
Quando não há correspondência com campanhas:  
canal → "Sem Campanha Ativa"  
id_campanha → "MKT_OUTROS"  
investimento → 0  
ref → "Sem Campanha / Orgânico"

**6. Data Modeling – Criação de Métricas**  
Arquivo: data_modeling.py  
Após as integrações, são criadas métricas financeiras principais e métricas auxiliares:

***Métricas financeiras (arredondadas para 2 casas decimais):***  
receita = quantidade × preco_unitario  
custo_total = quantidade × custo_unitario  
lucro = receita − custo_total  
margem_pct = (lucro / receita) * 100

> Motivo do arredondamento:
> Evita valores com muitas casas decimais (ex.: 18.899999 ou 145.777777), garantindo que os relatórios e CSVs finais fiquem legíveis e consistentes.

***Métricas auxiliares (não arredondadas):***  
ticket_venda = receita  
ano_mes = período Ano-Mês derivado de data_venda

**7. Geração de Dataset Final**  
Os arquivos finais são salvos em:  
data/processed/

Arquivos gerados:  
modern_beauty_vendas.csv  
modern_beauty_clientes_campanhas.csv

O script também exibe no terminal:
- Preview das vendas consolidadas
- Preview da base clientes + campanhas

## Decisões Técnicas do Projeto
**Uso de left join nas integrações**  
Todas as integrações entre tabelas foram realizadas utilizando how="left" no pandas.merge().

Motivação:
- Garantir que nenhum registro de venda seja perdido durante o processo de integração.
- Preservar a completude do dado transacional, mesmo que existam inconsistências nas tabelas auxiliares.
- Simular um cenário real de ambiente corporativo, onde dados dimensionais podem estar incompletos.
- Essa decisão prioriza integridade analítica sobre eliminação silenciosa de registros.

**Arquitetura Modular do Pipeline de Dados**
O pipeline foi dividido em módulos independentes organizados por responsabilidade:

***Schemas (Estrutura de Dados)***
- schemas.py

***Validação de Dados***
- validators.py

***Transformações (Scripts)***
- data_loader.py  
- data_cleaning.py  
- data_merging.py  
- data_modeling.py

Motivação:
- Separação clara de responsabilidades (schemas, validação e transformação)
- Facilidade de manutenção e leitura
- Possibilidade de reutilização das funções e regras de validação em outros projetos
- Organização semelhante a pipelines utilizados em ambientes produtivos
- Implementação de uma camada de qualidade de dados (data validation layer)
Essa estrutura permite escalabilidade futura, melhor governança do código e maior confiabilidade dos dados processados.

**Geração de CSVs Consolidados**  
Os datasets finais são exportados para a pasta data/processed/

Motivação:
- Separação entre camada de dados brutos (raw) e dados tratados (processed)
- Disponibilização de base estruturada para ferramentas de BI
- Possibilidade de auditoria e reprocessamento
- Simulação de uma camada analítica final (Data Mart simplificado)

**Separação entre Base de Vendas e Base de Clientes + Campanhas**  
O projeto gera dois datasets finais:
- Base consolidada de vendas com métricas financeiras
- Base de clientes integrada com campanhas de marketing

Motivação:
- Evitar duplicação desnecessária de dados de campanhas em cada transação
- Permitir análises específicas por domínio (financeiro vs marketing)
- Simular modelagem orientada a análises multidimensionais

Essa decisão melhora organização analítica e reduz redundância estrutural.

**Uso de Pydantic para Validação de Dados**  
Motivação:
- Garantir tipagem forte nos dados
- Evitar inconsistências silenciosas
- Centralizar regras de validação
- Aproximar o projeto de padrões utilizados em pipelines produtivos

**Implementação de Testes Automatizados (Pytest)**  
O projeto conta com testes automatizados para garantir a confiabilidade do pipeline.

Cobertura de testes:
- Limpeza de dados
- Carregamento de arquivos
- Validação de schemas
- Integridade estrutural dos dados
- Cálculo de métricas

Motivação:
- Prevenir regressões
- Garantir qualidade do código
- Simular práticas reais de engenharia de dados

## Resultado Final
O projeto entrega:
- Dataset consolidado de vendas com métricas financeiras
- Dataset de clientes com vínculo de campanhas
- Base estruturada para análises estratégicas
- Pipeline reproduzível e organizado de forma modular

## Competências Demonstradas
Este projeto demonstra experiência prática em:
- Estruturação de pipelines de dados
- Organização modular de código
- Tratamento de dados inconsistentes
- Modelagem analítica
- Integração entre múltiplas fontes
- Criação de métricas de negócio
- Preparação de dados para BI
- Validação de dados com Pydantic
- Testes automatizados com Pytest
- Monitoramento com logging
- Garantia de integridade estrutural de dados
- Boas práticas de versionamento (Git)

## Como Executar o Projeto:

**Instalar dependências:**  
pip install -r requirements.txt

**Executar o pipeline:**  
python main.py

**Executar testes:**  
pytest

O sistema irá:
1. Carregar os dados
2. Limpar inconsistências
3. Realizar os merges
4. Criar métricas
5. Gerar os arquivos finais