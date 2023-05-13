def get_handshake(client_name: str, remember: bool) -> dict:
    "Возвращаю словарь запроса на сервер. Проверка соединения"
    return {
        'header': {
            'title': 'get_handshake',
        },
        'payload' : {
            'msg': "Server, are you there?",
            'remember': remember, # сохранять базу данных пользователя на сервере
        },
        'signature': {
            'name': client_name.split()[0],
            'surname': client_name.split()[1],
        }
    }

def save_user_data(name, surname) -> dict:
    return {
        'name': name,
        'surname': surname,
    }

options = {
    'handshake': get_handshake, # проверка связи с сервером
    'remember_me': save_user_data, # сохранение пользовательских данных в файл
}

