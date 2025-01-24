import json
import logging
import os

import pandas as pd
import requests

# Configuração do logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ComexStatAPI:
    """
    Classe para interagir com a API do Comex Stat.

    Attributes:
        base_url (str): A URL base da API.
        headers (dict): Cabeçalhos HTTP para as requisições.
    """

    def __init__(self, base_url):
        """
        Inicializa a classe ComexStatAPI com a URL base da API.

        Args:
            base_url (str): A URL base da API.
        """
        self.base_url = base_url
        self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    def fetch_data(self, payload):
        """
        Faz uma requisição POST para a API com o payload fornecido e retorna os dados em formato JSON.

        Args:
            payload (dict): O payload da requisição contendo os parâmetros da consulta.

        Returns:
            dict: Os dados retornados pela API em formato JSON.
        """
        try:
            response = requests.post(self.base_url, headers=self.headers, data=json.dumps(payload), verify=True)
            response.raise_for_status()
            logging.info('Dados extraídos com sucesso.')
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logging.error(f'HTTP error occurred: {http_err}')
        except Exception as err:
            logging.error(f'Other error occurred: {err}')
        return None


def save_to_parquet(data, filename):
    """
    Salva os dados fornecidos em um arquivo Parquet na pasta 'data'.

    Args:
        data (dict): Os dados a serem salvos.
        filename (str): O nome do arquivo Parquet.
    """
    os.makedirs('data', exist_ok=True)
    filepath = os.path.join('data', filename)
    df = pd.DataFrame(data['data']['list'])
    df.to_parquet(filepath, index=False)
    logging.info(f'Dados salvos em {filepath}')


def extract():
    """
    Função principal que configura os payloads de exportação e importação,
    faz a extração dos dados da API e salva os dados em arquivos CSV.
    """
    url = 'https://api-comexstat.mdic.gov.br/general'

    export_payload = {
        'flow': 'export',
        'monthDetail': False,
        'period': {'from': '2024-01', 'to': '2024-12'},
        'filters': [{'filter': 'country', 'values': []}],
        'details': ['country', 'section', 'chapter', 'heading', 'subHeading'],
        'metrics': ['metricFOB', 'metricKG'],
    }

    import_payload = {
        'flow': 'import',
        'monthDetail': False,
        'period': {'from': '2024-01', 'to': '2024-12'},
        'filters': [{'filter': 'country', 'values': []}],
        'details': ['country', 'section', 'chapter', 'heading', 'subHeading'],
        'metrics': ['metricFOB', 'metricKG', 'metricFreight', 'metricInsurance', 'metricCIF'],
    }

    api = ComexStatAPI(url)

    # Extrair dados de exportação
    logging.info('Iniciando extração de dados de exportação...')
    export_data = api.fetch_data(export_payload)
    if export_data:
        logging.info('Processando dados de exportação...')
        save_to_parquet(export_data, 'export_data.parquet')
    else:
        logging.error('Falha ao extrair dados de exportação. Abortando...')
        return

    # Extrair dados de importação
    logging.info('Iniciando extração de dados de importação...')
    import_data = api.fetch_data(import_payload)
    if import_data:
        logging.info('Processando dados de importação...')
        save_to_parquet(import_data, 'import_data.parquet')
    else:
        logging.error('Falha ao extrair dados de importação.')
