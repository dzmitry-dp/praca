import socket
from threading import Thread

from dev.action.hash import hash_raw


SERVER = "167.71.37.89"
PORT = 1489

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def forever_listen_server():
    while True:
        try:
            print('Ожидаю сообщений')
            data =  client_socket.recv(4096)
            msg = data.decode('utf-8')

            if msg:
                print("Принято сообщение от сервера :" , msg)
            else:
                print("Принято сообщение от сервера :" , msg)
                print("Отключение клиента после сообщения msg = ''")
                client_socket.close()
                break
        except ConnectionAbortedError:
            print("\nОтключение клиента ConnectionAbortedError")
            client_socket.close()
            break

def send_client_name_to_server(client_name: str):
    hash_raw = hash_raw(client_name)
    client_socket.sendall(bytes(hash_raw, 'UTF-8'))
    print("Отпаравлено имя клиента:", client_name)

def connect_to_server():
    try:
        client_socket.connect((SERVER, PORT))
    except ConnectionRefusedError:
        print("Подключение не установлено")
        return False
    else:
        # поток для входящей информации
        input_thread = Thread(target=forever_listen_server)
        input_thread.start()
        # input_thread.join()
        return True

def start_client_server_dialog(user_name: str, user_surname: str):
    client_name = f'{user_name} {user_surname}'
    print('Start')
    if connect_to_server():
        # Поток для исходящей информации
        output_thread = Thread(target=send_client_name_to_server, args=[client_name,])
        output_thread.start()
        output_thread.join()
    
    print('End')
