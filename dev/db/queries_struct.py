from datetime import datetime

USER_BASE = 'user_base'

###
# Так выглядят данные на создание таблицы
###
user_table = {
    'table_name': USER_BASE,
    'column_data': {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'dt': 'TIMESTAMP',
        'name': 'TEXT',
        'surname': 'TEXT',
        'hour': 'REAL', # часы работы 
        'building': 'TEXT', # будова
        'helm': 'REAL', # часы за рулем
        'auto': 'INTEGER', # служебное авто 1 - True, 0 - False
        'start': 'INTEGER', # километраж начало
        'end': 'INTEGER', # киллометраж конец
        'es': 'INTEGER', # end - start = es
        }
    }
###
# Так выглядят данные на запись
###
def generate_first_data(name, surname):
    return {
        'table_name': USER_BASE,
        'column_data': {
            'dt': datetime.now(),
            'name': name,
            'surname': surname,
            'hour': None,
            'building': None,
            'helm': None,
            'auto': None, # 1 - True, 0 - False
            'start': None,
            'end': None,
            'es': None, # end - start = e-s
            }
        }
###
# Так выглядят данные на исправление
###
replace_data = {
    'table_name': 'zero_test',
    'column_data': {
        'dt': datetime.now(),
        'name': 'new',
        'surname': 'new',
        'id': 4 # последним стоит id т.к. в конце запроса стоит WHERE id = ?
        }
    }