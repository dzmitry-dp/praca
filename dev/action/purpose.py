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

def to_freeze_file(name, surname, payment_day, work_places = []) -> dict:
    return {
        'name': name,
        'surname': surname,
        'payment_day': payment_day,
        'work_places': work_places,
    }

options = {
    'handshake': get_handshake, # проверка связи с сервером
    'remember_me': to_freeze_file, # сохранение пользовательских данных в файл
}

