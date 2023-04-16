import sqlite3

import dev.action as action
from dev.action.exceptions import DBConnectionErr


def connection_to_database(create_query_func):
    def wrapper(self, **kwargs):
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
                cursor.execute(query)
                record = cursor.fetchall()
                return record
            elif 'CREATE' in query:
                values = list(kwargs['data']['column_data'].values())
                cursor.execute(query)

        except sqlite3.Error as error:
            raise DBConnectionErr(f"Error while connecting to database\n\n{error}")
        finally:
            connection.commit()
            connection.close()
    return wrapper

class Query:
    def __init__(self, db_path: str):
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
    def show_data_from_table(self, table_name: str):
        return f"SELECT * FROM {table_name};"
    
    @connection_to_database
    def remove_table(self, table_name: str):
        return f"DROP TABLE {table_name};"

    @connection_to_database
    def query_login_and_password(self, table_name: str, name: str, surname: str):
        return f"SELECT * FROM {table_name} WHERE name = '{name}' AND surname = '{surname}';"
