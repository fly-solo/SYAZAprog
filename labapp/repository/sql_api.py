from .connector import StoreConnector
from pandas import DataFrame, Series
from datetime import datetime

"""
    В данном модуле реализуется API (Application Programming Interface)
    для взаимодействия с БД с помощью объектов-коннекторов.
    
    ВАЖНО! Методы должны быть названы таким образом, чтобы по названию
    можно было понять выполняемые действия.
"""

# Вывод списка обработанных файлов с сортировкой по дате
def select_all_from_source_files(connector: StoreConnector):
    connector.start_transaction()  # начинаем выполнение запросов
    query = f'SELECT * FROM exchange_rates LIMIT 10000'
    result = connector.execute(query).fetchall()
    connector.end_transaction()  # завершаем выполнение запросов
    return result

# Вставка строк в таблицу flats_for_sale
def insert_rows_into_exchange_rates(connector: StoreConnector, df: DataFrame):
    connector.start_transaction()
    connector.execute(f'DELETE FROM exchange_rates;')
    connector.execute(f'UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME=\'exchange_rates\';')

    row_flats = df.to_dict('records')
    for row in row_flats:
        connector.execute(f'INSERT INTO exchange_rates (CountryCurrency, currency, value, Posted_On) '
                          f'VALUES ('
                          f'\'{row["CountryCurrency"]}\', \'{row["currency"]}\', \'{row["value"]}\', '
                          f'\'{row["Posted_On"]}\')')
    connector.end_transaction()
