from datetime import datetime

from dev.config import FIRST_TABLE, WORKER_TABLE

###
# Так выглядят данные на создание таблицы
###
user_table = {
    'table_name': FIRST_TABLE,
    'column_data': {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'dt': 'TIMESTAMP', # время добавление записи
        'name': 'TEXT',
        'surname': 'TEXT',
        'hour': 'INTEGER', # часы работы 
        'building': 'TEXT', # будова
        'date': 'TIMESTAMP', # дата указанная пользователем
        'auto': 'INTEGER', # служебное авто 1 - True, 0 - False
        'helm': 'REAL', # часы за рулем
        'start': 'INTEGER', # километраж начало
        'end': 'INTEGER', # киллометраж конец
        'es': 'INTEGER', # end - start = es
        }
    }

###
# Так выглядят данные на запись
###
def generate_data(user_name, user_surname, date, build_object, hour):
    return {
        'table_name': FIRST_TABLE,
        'column_data': {
            'dt': datetime.now(),
            'name': user_name,
            'surname': user_surname,
            'hour': hour,
            'building': build_object,
            'date': date,
            'auto': None, # 1 - True, 0 - False
            'helm': None,
            'start': None,
            'end': None,
            'es': None, # end - start = e-s
            }
        }
###
# Так выглядят данные на исправление
###
# replace_data = {
#     'table_name': 'zero_test',
#     'column_data': {
#         'dt': datetime.now(),
#         'name': 'new',
#         'surname': 'new',
#         'id': 4 # последним стоит id т.к. в конце запроса стоит WHERE id = ?
#         }
#     }

### 
# Данные на удаление
###
def get_date_to_remove(datetime_obj: datetime, building_object: str):
    return {
    'table_name': FIRST_TABLE,
    'column_data': {
        'building': building_object,
        'date': datetime_obj,
        }
    }
###
