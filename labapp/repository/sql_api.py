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
    query = f'SELECT * FROM source_files ORDER BY processed'
    result = connector.execute(query).fetchall()
    connector.end_transaction()  # завершаем выполнение запросов
    return result
