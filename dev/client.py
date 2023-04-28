import socket
import requests
from threading import Thread
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

from dev import action
from dev.action.targets import target_version
from dev.action.hash import hash_raw


SERVER = "167.71.37.89"
PORT = 1489

def select_msg(key: bytes, target: int):
    "Возвращаю зашифрованный json"
    action.logger.info('client.py: select_msg()')

    if target == None:
        target = 0

    action.logger.info(f"DEBUG: target message: {target_version[target]}")

    # Зашифровываем данные
    json_data = json.dumps(target_version[target])
    cipher = AES.new(key, AES.MODE_CBC, key[:16])
    padded_data = pad(json_data.encode('utf-8'), AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    
    action.logger.info(f"DEBUG: Encrypted data: {encrypted_data}")

    return encrypted_data

def forever_listen_server(client_socket: socket.socket):
    action.logger.info('client.py: forever_listen_server()')

    while True:
        try:
            action.logger.info(f"client.py: I'm waiting for a message from the {SERVER}")
            data =  client_socket.recv(4096)
            msg = data.decode('utf-8')

            if not msg:
                action.logger.info(f"DEBUG: Shutting down the server after a message = {msg}")
                break

            action.logger.info(f"DEBUG: Message from the {SERVER} : {msg}")
        except ConnectionAbortedError:
            action.logger.error(f"ConnectionAbortedError")
            break
    
    client_socket.close()
    

def send_msg_to_server(client_name: str, client_ip: str, client_socket: socket.socket, key: bytes, target: int):
    action.logger.info('client.py: send_client_name_to_server()')

    msg: bytes = select_msg(key, target) # зашифрованный json
    client_socket.sendall(msg)

    action.logger.info(f"DEBUG: client_name: '{client_name}', client_ip: '{client_ip}")

def connect_to_server(client_socket):
    try:
        action.logger.info(f'client.py: Try connect to {SERVER}:{PORT}')
        client_socket.connect((SERVER, PORT))
    except ConnectionRefusedError:
        action.logger.error('client.py: ConnectionRefusedError - Not connections')
        return False
    else:
        action.logger.info(f'client.py: Connected to {SERVER}:{PORT}')
        ### Отдельным потоком принимаем входящую информацию
        input_thread = Thread(target = forever_listen_server, daemon = True, name = 'input_thread', args = [client_socket,])
        input_thread.start()
        ###
        return True

def start_client_server_dialog(user_name: str, user_surname: str, display_main_screen_thread: Thread = None, target: str = None):
    action.logger.info('client.py: start_client_server_dialog()')
    response = requests.get("http://ifconfig.me/ip")
    client_name = f'{user_name} {user_surname}'
    client_ip = response.text
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    key: bytes = hash_raw(client_ip, PORT)

    action.logger.info(f"DEBUG: IP '{client_ip}")
    action.logger.info(f"DEBUG: key = {key}")

    if connect_to_server(client_socket):
        # Поток для исходящей информации
        output_thread = Thread(
            target = send_msg_to_server,
            args = [client_name, client_ip, client_socket, key, target],
            daemon = True,
            name = 'output_thread',
            )
        output_thread.start()
        output_thread.join() # жду пока не ответит сервер

    if display_main_screen_thread is not None:
        display_main_screen_thread.join()
