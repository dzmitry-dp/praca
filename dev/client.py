import socket
import requests
from threading import Thread

from dev import action
from dev.action.hash import hash_raw


SERVER = "167.71.37.89"
PORT = 1489


def forever_listen_server(client_socket):
    action.logger.info('client.py: forever_listen_server()')
    while True:
        try:
            action.logger.info("client.py: I'm waiting for a message from the SERVER")
            data =  client_socket.recv(4096)
            msg = data.decode('utf-8')

            if not msg:
                action.logger.info(f"DEBUG: Shutting down the server after a message = {msg}")
                client_socket.close()
                break

            action.logger.info(f"DEBUG: Message from SERVER = {msg}")
        except ConnectionAbortedError:
            action.logger.error(f"ConnectionAbortedError")
            client_socket.close()
            break

def send_client_name_to_server(client_name: str, client_socket):
    action.logger.info('client.py: send_client_name_to_server()')
    raw = hash_raw(client_name, PORT)
    client_socket.sendall(bytes(raw, 'UTF-8'))

def connect_to_server(client_socket):
    try:
        action.logger.info('client.py: Try connect to SERVER:PORT')
        client_socket.connect((SERVER, PORT))
    except ConnectionRefusedError:
        action.logger.error('client.py: ConnectionRefusedError - Not connections')
        return False
    else:
        action.logger.info('client.py: Connect to SERVER:PORT')
        ### Отдельным потоком принимаем входящую информацию
        input_thread = Thread(target = forever_listen_server, daemon = True, name = 'input_thread', args = [client_socket,])
        input_thread.start()
        ###
        return True

def start_client_server_dialog(user_name: str, user_surname: str, display_main_screen_thread):
    action.logger.info('client.py: start_client_server_dialog()')
    response = requests.get("http://ifconfig.me/ip")
    client_name = response.text # ip

    action.logger.info(f"DEBUG: IP '{client_name}")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if connect_to_server(client_socket):
        # Поток для исходящей информации
        output_thread = Thread(
            target = send_client_name_to_server,
            args = [client_name, client_socket,],
            daemon = True,
            name = 'output_thread',
            )
        output_thread.start()
        output_thread.join() # жду пока не ответит сервер
    
    display_main_screen_thread.join()
