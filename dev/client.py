import socket
import requests
from threading import Thread
import json
from cryptography.fernet import Fernet

from dev import action
from dev.action.purpose import options
from dev.action.hash import hash_raw
from dev.ftp_client import connect_to_ftp
import dev.config as config


def thread_control(start_client_server_dialog):
    action.logger.info('client.py: thread_control()')
    def wrapper(**kwargs):
        action.logger.info('client.py: @thread_control')
        if kwargs['msg_purpose'] == 'handshake':
            # первый запуск после логирования / handshake
            start_client_server_dialog(**kwargs)
    return wrapper

class Client:
    @thread_control
    def start_client_server_dialog(
        user_name: str,
        user_surname: str,
        remember_me: bool, # галочка Запомнить меня на экране авторизации
        msg_purpose: str, # цель с которой связывается клиент с сервером
        ):
        """
        msg_purpose - цель обращения к серверу
        """
        action.logger.info('client.py: start_client_server_dialog()')
        response = requests.get("http://ifconfig.me/ip")
        client_name: str = f'{user_name} {user_surname}'
        client_ip = response.text
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        key: bytes = hash_raw(client_ip, config.PORT)

        action.logger.info(f"DEBUG: IP '{client_ip}'")
        action.logger.info(f"DEBUG: key = {key}")

        if _connect_to_server(client_socket, key):
            ### Отдельный поток для информации
            send_json_msg_thread = Thread(
                name = 'send_json_msg_thread',
                target = _send_json_msg_to_server,
                daemon = True,
                args = [client_name, client_ip, client_socket, key, msg_purpose, remember_me],
                )
            send_json_msg_thread.start()
            send_json_msg_thread.join() # жду пока не закончим диалог с сервером
            ###

def _connect_to_server(client_socket, key) -> bool:
    action.logger.info('client.py: _connect_to_server()')
    try:
        action.logger.info(f'DEBUG: Try connect to {config.SERVER}:{config.PORT}')
        client_socket.connect((config.SERVER, config.PORT))
    except ConnectionRefusedError:
        action.logger.error('client.py: ConnectionRefusedError - Not connections')
        return False
    except TimeoutError:
        action.logger.error('client.py: TimeoutError - Not connections')
        return False
    else:
        action.logger.info(f'DEBUG: Connected to {config.SERVER}:{config.PORT}')
        ### Отдельным потоком принимаем входящую информацию
        listen_thread = Thread(target = _forever_listen_server, daemon = True, name = 'listen_thread', args = [client_socket, key,])
        listen_thread.start()
        ###
        return True

def _get_reply_msg(client_name: str, key: bytes, msg_purpose: str, remember_me: bool) -> bytes:
    "Возвращаю зашифрованный json"
    action.logger.info('client.py: _get_reply_msg()')

    # Зашифровываем данные
    f = Fernet(key)
    json_data = json.dumps(options[msg_purpose](client_name, remember_me))
    encrypted_data = f.encrypt(json_data.encode('utf-8'))
    
    return encrypted_data

def _send_json_msg_to_server(client_name: str, client_ip: str, client_socket: socket.socket, key: bytes, msg_purpose: str, remember_me: bool):
    action.logger.info('client.py: _send_json_msg_to_server()')
    
    msg: bytes = _get_reply_msg(client_name, key, msg_purpose, remember_me) # зашифрованный json
    client_socket.sendall(msg)

def _forever_listen_server(client_socket: socket.socket, key: bytes):
    action.logger.info('client.py: _forever_listen_server()')

    def select_client_reaction(decode_data):
        print(type(decode_data))
        action.logger.info('client.py: select_client_reaction()')
        if decode_data == '':
            client_socket.close()
        else:
            decode_data = json.loads(decode_data)

        if decode_data['header']['title'] == 'send_ssl_port':
            pass

        if decode_data['signature']['update']: # если сервер предлагает обновить базы данных
            connect_to_ftp(
                purpose = 'update', # цель соединения с ftp сервером
                port = decode_data['payload']['ftp_port'],
                login  = decode_data['header']['name'],
                password = decode_data['header']['surname'],
                cert = decode_data['payload']['cert'],
                path_to_employer_base = decode_data['payload']['employer_base'],
                )

    while True:
        try:
            action.logger.info(f"DEBUG: I'm waiting for a message from the {config.SERVER}")
            data_from_server =  client_socket.recv(4096)

            if not data_from_server: # if data_from_server == '' -> break
                action.logger.info(f"DEBUG: Shutting down the server after a message = {data_from_server}")
                break
            else:
                # Расшифровываем данные
                f = Fernet(key)
                decrypted_data = f.decrypt(data_from_server)
                decode_data: dict = json.loads(decrypted_data.decode('utf-8'))

                action.logger.info(f"DEBUG: decode_data = {decode_data}")
                select_client_reaction(decode_data)

        except ConnectionAbortedError:
            action.logger.error(f"ConnectionAbortedError")
            break
    
    client_socket.close()
