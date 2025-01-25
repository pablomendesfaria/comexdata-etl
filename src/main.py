import subprocess

from extract.comex_stat_api import extract
from load.snowflake_loader import load


def transform():
    """
    Executa o comando dbt run para aplicar as transformações definidas nos modelos dbt.
    """
    try:
        result = subprocess.run(['dbt', 'run --project-dir src/transform/'], check=True, capture_output=True, text=True)
        print(result.stdout)
        print('Transformações dbt executadas com sucesso.')
    except subprocess.CalledProcessError as e:
        print(f'Erro ao executar dbt run: {e.stderr}')


if __name__ == '__main__':
    extract()
    load()
    transform()
