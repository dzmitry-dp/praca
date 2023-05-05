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

options = {
    'handshake': get_handshake, # проверка связи с сервером
}

