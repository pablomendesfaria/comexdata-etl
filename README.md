# ComexData ETL Project

## Descrição

Este projeto é um pipeline de ETL (Extração, Transformação e Carga) para dados de comércio exterior do Brasil, utilizando a API do Comex Stat. O pipeline extrai dados de importação e exportação, carrega-os no Snowflake, e aplica transformações utilizando dbt (data build tool). O objetivo é fornecer uma estrutura de dados dimensional para análise de dados de comércio exterior.

## Estrutura do Projeto

```
comexdata-etl/
├── data/                           # Diretório para armazenar arquivos de dados
│   ├── export_data.parquet
│   └── import_data.parquet
├── src/
│   ├── extract/
│   │   └── comex_stat_api.py       # Script para extrair dados da API do Comex Stat
│   ├── load/
│   │   └── snowflake_loader.py     # Script para carregar dados no Snowflake
│   ├── transform/
│   │   ├── dbt_project.yml         # Configuração do projeto dbt
│   │   ├── models/
│   │   │   ├── marts/
│   │   │   │   └── core/
│   │   │   │       ├── dim_sections.sql
│   │   │   │       ├── dim_chapters.sql
│   │   │   │       ├── dim_headings.sql
│   │   │   │       ├── dim_subheadings.sql
│   │   │   │       ├── dim_countries.sql
│   │   │   │       ├── fact_imports.sql
│   │   │   │       ├── fact_exports.sql
│   │   │   ├── staging/
│   │   │   │   └── snowflake/
│   │   │   │       ├── stg_snowflake__imports.sql
│   │   │   │       ├── stg_snowflake__exports.sql
│   │   ├── models/
│   │   │   ├── marts/
│   │   │   │   └── core/
│   │   │   │       ├── dim_sections.yml
│   │   │   │       ├── dim_chapters.yml
│   │   │   │       ├── dim_headings.yml
│   │   │   │       ├── dim_subheadings.yml
│   │   │   │       ├── dim_countries.yml
│   │   │   │       ├── fact_imports.yml
│   │   │   │       ├── fact_exports.yml
│   │   │   ├── staging/
│   │   │   │   └── snowflake/
│   │   │   │       ├── stg_snowflake.yml
│   │   │   │       ├── src_raw_schema.yml
│   ├── main.py                     # Script principal para executar o pipeline ETL
├── .env                            # Arquivo de configuração de variáveis de ambiente
├── pyproject.toml                  # Dependências do projeto
└── README.md                       # Documentação do projeto
```

## Pré-requisitos

- Python 3.8 ou superior
- Poetry
- Snowflake
- dbt (data build tool)
- Biblioteca python-dotenv para carregar variáveis de ambiente

## Configuração

### 1. Clonar o Repositório

```
git clone https://github.com/seu-usuario/comexdata-etl.git
cd comexdata-etl
```

### 2. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis de ambiente:

```
SNOWFLAKE_USER=seu_usuario
SNOWFLAKE_PASSWORD=sua_senha
SNOWFLAKE_ACCOUNT=seu_conta
SNOWFLAKE_WAREHOUSE=seu_warehouse
SNOWFLAKE_DATABASE=seu_database
SNOWFLAKE_SCHEMA=raw_schema
SNOWFLAKE_ROLE=seu_role
```
### 3. Instalar Dependências

```
poetry install
```

### 4. Configurar o dbt

Crie um arquivo `profiles.yml` no diretório `~/.dbt/` com a seguinte configuração:

```
dbt_comexstat_project:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: "{{ env_var('SNOWFLAKE_ACCOUNT') }}"
      user: "{{ env_var('SNOWFLAKE_USER') }}"
      password: "{{ env_var('SNOWFLAKE_PASSWORD') }}"
      role: "{{ env_var('SNOWFLAKE_ROLE') }}"
      database: "{{ env_var('SNOWFLAKE_DATABASE') }}"
      warehouse: "{{ env_var('SNOWFLAKE_WAREHOUSE') }}"
      schema: "{{ env_var('SNOWFLAKE_SCHEMA') }}"
      threads: 4
      client_session_keep_alive: False
```

## Execução do Pipeline ETL

### 1. Extrair Dados da API

O script `comex_stat_api.py` extrai dados de importação e exportação da API do Comex Stat e salva-os em arquivos Parquet no diretório `data`.

### 2. Carregar Dados no Snowflake
O script `snowflake_loader.py` carrega os arquivos Parquet no Snowflake, criando e populando as tabelas `export_table` e `import_table`.

### 3. Transformar Dados com dbt
O script `main.py` executa as etapas de extração, carregamento e transformação dos dados. Para executar o pipeline completo, execute:

```
task run
```

### 4. Análise dos Dados

Após a execução do pipeline, os dados estarão disponíveis no Snowflake em uma estrutura dimensional, pronta para análise. Você pode usar ferramentas de BI como Tableau, Power BI ou Looker para criar dashboards e relatórios interativos.

## Estrutura das Tabelas

### Tabelas de Dimensões

- **dim_sections**: Tabela de dimensões para seções do SH.
- **dim_chapters**: Tabela de dimensões para capítulos do SH.
- **dim_headings**: Tabela de dimensões para headings do SH.
- **dim_subheadings**: Tabela de dimensões para subheadings do SH.
- **dim_countries**: Tabela de dimensões para países.

### Tabelas de Fatos

- **fact_imports**: Tabela de fatos para registros de importações.
- **fact_exports**: Tabela de fatos para registros de exportações.

## Testes de Qualidade dos Dados

O dbt é configurado para executar testes de qualidade dos dados, garantindo a integridade e a precisão dos dados carregados e transformados.