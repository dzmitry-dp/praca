import socket
import requests
from threading import Thread
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from dev import action
from dev.action.purpose import options
from dev.action.hash import hash_raw
from dev.ftp_client import connect_to_ftp


SERVER = "167.71.37.89"
PORT = 1489

def thread_control(start_client_server_dialog):
    def wrapper(**kwargs):
        if len(kwargs) == 2:
            # первый запуск после логирования / handshake
            action.logger.info(f'client.py: thread_control() have NOT thread')
            # kwargs = user_name: str, user_surname: str,
            start_client_server_dialog(**kwargs)
    return wrapper

class Client:
    @thread_control
    def start_client_server_dialog(user_name: str, user_surname: str, thread: Thread = None, msg_purpose: str = None):
        action.logger.info('client.py: start_client_server_dialog()')
        response = requests.get("http://ifconfig.me/ip")
        client_name = f'{user_name} {user_surname}'
        client_ip = response.text
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        key: bytes = hash_raw(client_ip, PORT)

        action.logger.info(f"DEBUG: IP '{client_ip}'")
        action.logger.info(f"DEBUG: key = {key}")

        if _connect_to_server(client_socket, key):
            ### Отдельный поток для информации
            send_json_msg_thread = Thread(
                target = _send_json_msg_to_server,
                args = [client_name, client_ip, client_socket, key, msg_purpose],
                daemon = True,
                name = 'send_json_msg_thread',
                )
            send_json_msg_thread.start()
            send_json_msg_thread.join() # жду пока не закончим диалог с сервером сервер
            ###

def _connect_to_server(client_socket, key) -> bool:
    try:
        action.logger.info(f'client.py: Try connect to {SERVER}:{PORT}')
        client_socket.connect((SERVER, PORT))
    except ConnectionRefusedError:
        action.logger.error('client.py: ConnectionRefusedError - Not connections')
        return False
    else:
        action.logger.info(f'client.py: Connected to {SERVER}:{PORT}')
        ### Отдельным потоком принимаем входящую информацию
        listen_thread = Thread(target = _forever_listen_server, daemon = True, name = 'listen_thread', args = [client_socket, key,])
        listen_thread.start()
        ###
        return True

def _get_reply_msg(client_name: str, key: bytes, msg_purpose: str) -> bytes:
    "Возвращаю зашифрованный json"
    action.logger.info('client.py: _get_reply_msg()')

    if msg_purpose == None:
        msg_purpose = 'handshake' # рукопожатие / проверка связи с сервером / получение адреса для передачи данных

    # Зашифровываем данные
    cipher = AES.new(key, AES.MODE_CBC, b'\x00'*16)
    json_data = json.dumps(options[msg_purpose](client_name))
    padded_data = pad(json_data.encode('utf-8'), AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    
    return encrypted_data

def _send_json_msg_to_server(client_name: str, client_ip: str, client_socket: socket.socket, key: bytes, msg_purpose: str):
    action.logger.info('client.py: _send_json_msg_to_server()')

    msg: bytes = _get_reply_msg(client_name, key, msg_purpose) # зашифрованный json
    client_socket.sendall(msg)

def _forever_listen_server(client_socket: socket.socket, key: bytes):
    action.logger.info('client.py: _forever_listen_server()')

    def select_client_reaction(decode_data):
        action.logger.info('client.py: select_client_reaction()')
        if decode_data == '':
            client_socket.close()
        elif decode_data['header']['title'] == 'send_ssl_port':
            pass

        if decode_data['signature']['update']: # если сервер предлагает обновить базы данных
            connect_to_ftp(
                purpose = 'update',
                port = decode_data['payload']['ftp_port'],
                login  = decode_data['header']['name'],
                password = decode_data['header']['surname'],
                cert = decode_data['payload']['cert'],
                path_to_employer_base = decode_data['payload']['employer_base'],
                )

    while True:
        try:
            action.logger.info(f"client.py: I'm waiting for a message from the {SERVER}")
            encrypted_data =  client_socket.recv(4096)

            if not encrypted_data: # if encrypted_data == '' -> break
                action.logger.info(f"DEBUG: Shutting down the server after a message = {encrypted_data}")
                break
            else:
                # Расшифровываем данные
                cipher = AES.new(key, AES.MODE_CBC, b'\x00'*16)
                decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
                # json.loads(decrypted_data.decode('utf-8')) почему-то str
                decode_data: json = json.loads(json.loads(decrypted_data.decode('utf-8')))

                action.logger.info(f"DEBUG: decode_data = {decode_data}")
                
                select_client_reaction(decode_data)

        except ConnectionAbortedError:
            action.logger.error(f"ConnectionAbortedError")
            break
    
    client_socket.close()
