import socket
import requests
from threading import Thread
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from dev import action
from dev.action.purpose import options
from dev.action.hash import hash_raw


SERVER = "167.71.37.89"
PORT = 1489

def select_msg(client_name: str, key: bytes, msg_purpose: int) -> bytes:
    "Возвращаю зашифрованный json"
    action.logger.info('client.py: select_msg()')

    if msg_purpose == None:
        msg_purpose = 0 # рукопожатие / проверка связи с сервером / получение адреса для передачи данных

    # Зашифровываем данные
    cipher = AES.new(key, AES.MODE_CBC, b'\x00'*16)
    json_data = json.dumps(options[msg_purpose](client_name))
    padded_data = pad(json_data.encode('utf-8'), AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    
    return encrypted_data

def forever_listen_server(client_socket: socket.socket, key: bytes):
    action.logger.info('client.py: forever_listen_server()')

    def select_client_reaction(decode_data):
        if decode_data['header']['title'] == 'send_ssl_port':
            # у нас есть порт по которому настроен ftp
            # скачать актуальную базу
            pass

    while True:
        try:
            action.logger.info(f"client.py: I'm waiting for a message from the {SERVER}")
            encrypted_data =  client_socket.recv(4096)

            if not encrypted_data:
                action.logger.info(f"DEBUG: Shutting down the server after a message = {encrypted_data}")
                break
            else:
                # Расшифровываем данные
                cipher = AES.new(key, AES.MODE_CBC, b'\x00'*16)
                decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
                decode_data: json = json.loads(decrypted_data.decode('utf-8'))

                action.logger.info(f"DEBUG: decode_data = {decode_data}")
                
                select_client_reaction(decode_data)

        except ConnectionAbortedError:
            action.logger.error(f"ConnectionAbortedError")
            break
    
    client_socket.close()
    

def send_json_msg_to_server(client_name: str, client_ip: str, client_socket: socket.socket, key: bytes, msg_purpose: int):
    action.logger.info('client.py: send_json_msg_to_server()')

    msg: bytes = select_msg(client_name, key, msg_purpose) # зашифрованный json
    client_socket.sendall(msg)

def connect_to_server(client_socket, key):
    try:
        action.logger.info(f'client.py: Try connect to {SERVER}:{PORT}')
        client_socket.connect((SERVER, PORT))
    except ConnectionRefusedError:
        action.logger.error('client.py: ConnectionRefusedError - Not connections')
        return False
    else:
        action.logger.info(f'client.py: Connected to {SERVER}:{PORT}')
        ### Отдельным потоком принимаем входящую информацию
        input_thread = Thread(target = forever_listen_server, daemon = True, name = 'input_thread', args = [client_socket, key,])
        input_thread.start()
        ###
        return True

def thread_control(client_server_dilog):
    def wrapper(**kwargs):
        if kwargs.thread.name == 'handshake_thread':
            client_server_dilog(**kwargs)
            kwargs.thread.join()
        elif kwargs.thread.name == 'download_thread':
            kwargs.thread.join()
            client_server_dilog(**kwargs)
    return wrapper

@thread_control
def start_client_server_dialog(user_name: str, user_surname: str, thread: Thread = None, msg_purpose: str = None):
    action.logger.info('client.py: start_client_server_dialog()')
    response = requests.get("http://ifconfig.me/ip")
    client_name = f'{user_name} {user_surname}'
    client_ip = response.text
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    key: bytes = hash_raw(client_ip, PORT)

    action.logger.info(f"DEBUG: IP '{client_ip}")
    action.logger.info(f"DEBUG: key = {key}")

    if connect_to_server(client_socket, key):
        # Поток для исходящей информации
        output_thread = Thread(
            target = send_json_msg_to_server,
            args = [client_name, client_ip, client_socket, key, msg_purpose],
            daemon = True,
            name = 'output_thread',
            )
        output_thread.start()
        output_thread.join() # жду пока не ответит сервер
