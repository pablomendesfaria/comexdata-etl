import logging
import os

import snowflake.connector
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração do logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def create_table_if_not_exists(cursor: snowflake.connector.cursor, table_name: str, columns: str):
    """
    Cria uma tabela no Snowflake se ela não existir.

    Args:
        cursor (snowflake.connector.cursor): O cursor do Snowflake.
        table_name (str): O nome da tabela.
        columns (str): A definição das colunas da tabela.
    """
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        {columns}
    )
    """
    cursor.execute(create_table_query)
    logging.info(f'Tabela {table_name} verificada/criada com sucesso.')


def load_parquet_to_snowflake(cursor: snowflake.connector.cursor, file_path: str, table_name: str, columns: str):
    """
    Carrega um arquivo Parquet para uma tabela no Snowflake.

    Args:
        cursor (snowflake.connector.cursor): O cursor do Snowflake.
        file_path (str): O caminho do arquivo Parquet.
        table_name (str): O nome da tabela no Snowflake.
        columns (str): A definição das colunas da tabela.
    """
    try:
        create_table_if_not_exists(cursor, table_name, columns)
        cursor.execute(f'TRUNCATE TABLE {table_name}')  # Limpar a tabela antes de carregar os dados
        cursor.execute(f'PUT file://{os.path.abspath(file_path)} @%{table_name}')
        cursor.execute(
            f"COPY INTO {table_name} FROM @%{table_name} FILE_FORMAT = (TYPE = 'PARQUET') MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE"
        )
        logging.info(f'Dados carregados em {table_name} com sucesso.')
    except Exception as e:
        logging.error(f'Erro ao carregar dados: {e}')


def load():
    """
    Função principal que carrega os arquivos CSV de exportação e importação para o Snowflake.
    """
    conn_params = {
        'user': os.getenv('SNOWFLAKE_USER'),
        'password': os.getenv('SNOWFLAKE_PASSWORD'),
        'account': os.getenv('SNOWFLAKE_ACCOUNT'),
        'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
        'database': os.getenv('SNOWFLAKE_DATABASE'),
        'schema': os.getenv('SNOWFLAKE_SCHEMA'),
        'role': os.getenv('SNOWFLAKE_ROLE'),
    }

    export_columns = """
    coNcmSecrom STRING,
    year INT,
    country STRING,
    section STRING,
    chapterCode INT,
    chapter STRING,
    headingCode INT,
    heading STRING,
    subHeadingCode INT,
    subHeading STRING,
    metricFOB FLOAT,
    metricKG FLOAT
    """

    import_columns = """
    coNcmSecrom STRING,
    year INT,
    country STRING,
    sectionCode INT,
    section STRING,
    chapterCode INT,
    chapter STRING,
    headingCode INT,
    heading STRING,
    subHeadingCode INT,
    subHeading STRING,
    metricFOB FLOAT,
    metricKG FLOAT,
    metricFreight FLOAT,
    metricInsurance FLOAT,
    metricCIF FLOAT
    """

    with snowflake.connector.connect(**conn_params) as conn:
        with conn.cursor() as cursor:
            # Carregar dados de exportação
            load_parquet_to_snowflake(cursor, 'data/export_data.parquet', 'export_table', export_columns)

            # Carregar dados de importação
            load_parquet_to_snowflake(cursor, 'data/import_data.parquet', 'import_table', import_columns)
