import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .processor.dataprocessorfactory import *
from .repository.connectorfactory import *       # подключаем фабрику коннекторов к БД
from .repository.sql_api import *
from config import *
"""
Модуль с описанием ORM-моделей базы данных
"""

# Подключение объекта для управления БД
#from labapp import db


# В зависимости от расширения файла вызываем соответствующий фабричный метод
def init_processor(source: str) -> DataProcessor:
    proc = None
    if source.endswith('.csv'):
        proc = CsvDataProcessorFactory().get_processor(source)
    elif source.endswith('.txt'):
        proc = TxtDataProcessorFactory().get_processor(source)
    else:
        proc = NoneDataProcessorFactory().get_processor(source)
    return proc

# Запуск обработки
def run_processor(proc: DataProcessor): # -> DataFrame:
    proc.run()
    #proc.print_result()
    # list_result = [proc.result_country, proc.result_year, proc.result_age]

def insert_processed_data_in_DB(DATASOURCE: str):
    proc = init_processor(DATASOURCE)
    if proc is not None:
        run_processor(proc)
        if proc.result is not None:
            db_connector = SQLStoreConnectorFactory().get_connector(DATABASE_URI)  # получаем объект соединения
            insert_rows_into_exchange_rates(db_connector, proc.result)
            # Завершаем работу с БД
            db_connector.close()
    else:
        pass

# Удаление ВСЕХ таблиц в БД и создание чистых таблиц по заданным моделям
#def reset_database():
#    db.delete_all()
#    db.create_all()