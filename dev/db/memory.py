import os
import json
import sqlite3
from datetime import datetime, timedelta

import dev.action as action
import dev.config as config
from dev.action.exceptions import DBConnectionErr


class MemoryDataContainer:
    """
    # Данные которые помнит приложение
    ## Получаю постепенно / НЕ сразу, а частями
    ### По мере использования пользователем приложения, данные перезаписываются в этот объект

    self.path_to_freeze_file: str путь до файла в котором хранятся данные пользователя

    self.user_data_from_db: list[tuple, ] данные считанные с базы данных

    """
    def __init__(self) -> None:
        action.logger.info(f"memory.py: class MemoryDataContainer def __init__()")
        self.path_to_freeze_file: str = None # путь к файлу, который хранит данные о текущем пользователе приложения
        self._freeze_file_data: dict = None
        self.user_data_from_db: list[tuple,] = None ### это поле заполняется с потока где считываются данные пользователя из базы данные

    @property
    def freeze_file_data(self) -> dict:
        if self._freeze_file_data is None:
            self._freeze_file_data = self.get_freeze_member()
        return self._freeze_file_data
  
    def get_freeze_member(self) -> dict:
        action.logger.info('memory.py: get_freeze_member()')
        # список всех файлов в папке
        files = os.listdir(config.PATH_TO_REMEMBER_ME)
        # фильтрация файлов по расширению
        jf = [file for file in files if file.endswith('.json')]
        
        if len(jf) == 1: # если в папке всего один json файл
            action.logger.info(f'DEBUG: Have json file {jf}')
            self.path_to_freeze_file = os.path.join(config.PATH_TO_REMEMBER_ME, f'{jf[0]}')
            with open(self.path_to_freeze_file, 'r') as file:
                freeze_file_data = json.load(file)
        else: # если нет файлов или нужно выбирать из нескольких
            action.logger.info(f'DEBUG: Have NOT json files')
            freeze_file_data = None

        return freeze_file_data

def connection_to_database(create_query_func):
    action.logger.info(f"memory.py: @connection_to_database")
    def wrapper(self, **kwargs):
        action.logger.info(f"memory.py: @connection_to_database -> wrapper()")
        try:
            connection = sqlite3.connect(
                self.db_path,
                detect_types=sqlite3.PARSE_DECLTYPES |
                                sqlite3.PARSE_COLNAMES
                ) 
            cursor = connection.cursor()
            query = create_query_func(self, **kwargs)
            
            action.logger.info(f'DEBUG: {query}')
            
            if 'INSERT' in query:
                values = list(kwargs['data']['column_data'].values())
                cursor.execute(query, values)
            elif 'UPDATE' in query:
                values = list(kwargs['data']['column_data'].values())
                cursor.execute(query, values)
            elif 'SELECT' in query:
                if 'DELETE' in query:
                    values = list(kwargs['data']['column_data'].values())
                    cursor.execute(query, values)
                    return None
                if 'payment_day' in kwargs.keys():
                    current_date = datetime.now().date()
                    start_date = datetime(current_date.year, current_date.month, kwargs['payment_day'])
                    end_date = start_date.replace(day=kwargs['payment_day']) + timedelta(days=31)
                    cursor.execute(query, (start_date, end_date))
                    record = cursor.fetchall()
                    return record
                cursor.execute(query)
                record = cursor.fetchall()
                return record
            elif 'CREATE' in query:
                values = list(kwargs['data']['column_data'].values())
                cursor.execute(query)
            elif 'DELETE' in query:
                values = list(kwargs['data']['column_data'].values())
                cursor.execute(query, values)
        except sqlite3.Error as error:
            raise DBConnectionErr(f"Error while connecting to database\n\n{error}")
        finally:
            connection.commit()
            connection.close()
    return wrapper

class QueryToSQLite3:
    def __init__(self, db_path: str):
        action.logger.info(f"memory.py: class QueryToSQLite3 def __init__() path: {db_path}")
        self.db_path = db_path
        self.query = ''
    
    @connection_to_database
    def create_table(self, data: dict):
        table_name: str = data['table_name']
        columns_and_types: dict = data['column_data']

        for column in columns_and_types.keys():
            self.query += f"{column} {columns_and_types[column]}, "

        return f"CREATE TABLE IF NOT EXISTS {table_name}({self.query[:-2]});"

    @connection_to_database
    def write_values(self, data: dict):     
        table_name: str = data['table_name']
        columns = list(data['column_data'].keys())
        values = list(data['column_data'].values())
        _ = '?, ' * len(values)
        return f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({_[:-2]});"

    @connection_to_database
    def replace_values(self, data: dict):
        table_name: str = data['table_name']
        columns = list(data['column_data'].keys())
        values = list(data['column_data'].values())
        return f'UPDATE {table_name} SET {", ".join([col_name + " = ?" for col_name in columns[:-1]])} WHERE id = ?'''     
    
    @connection_to_database
    def show_all_tables_in_db(self):
        return """SELECT name FROM sqlite_master WHERE type='table';"""
    
    @connection_to_database
    def show_data_from_table(self, table_name: str, payment_day: int):
        return f"SELECT * FROM {table_name} WHERE date >= ? AND date <= ? ORDER BY date;"
    
    @connection_to_database
    def remove_table(self, table_name: str):
        return f"DROP TABLE {table_name};"

    @connection_to_database
    def query_login_and_password(self, table_name: str, name: str, surname: str):
        return f"SELECT * FROM {table_name} WHERE name = '{name}' AND surname = '{surname}';"

    @connection_to_database
    def remove_row(self, data: dict):
        table_name = data['table_name']
        return f'DELETE FROM {table_name} WHERE id = (SELECT id FROM {table_name} WHERE building = ? AND date = ?);'
