from extract.comex_stat_api import extract
from load.snowflake_loader import load

if __name__ == '__main__':
    extract()
    load()
