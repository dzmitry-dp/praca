def get_handshake(client_name: str) -> dict:
    "Возвращаю словарь запроса на сервер. Проверка соединения"
    return {
        'header': {
            'title': 'get_handshake',
        },
        'payload' : {
            'msg': "Server, are you there?",
        },
        'signature': {
            'name': client_name.split()[0],
            'surname': client_name.split()[1],
        }
    }

def download_employer_database(client_name: str):
    "Запрос на скачивание файла базы данных работодателя"
    return {
        # Заголовок
        'header': {
            'title': 'download_employer_database',
        },
        # Полезная загрузка
        'payload' : {
            'msg': "I want to get fresh database",
            'cmd': "",
            },
        # Подпись
        'signature': {
            'name': client_name.split()[0],
            'surname': client_name.split()[1],
        }
    }

options = {
    0: get_handshake, # проверка связи с сервером
    1: download_employer_database, # загрузка свежей базы данных
}

