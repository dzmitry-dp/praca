import socket
from threading import Thread


SERVER = "159.223.25.102"
PORT = 1489

def listen_server():
    while True:
        try:
            in_data =  client.recv(4096)
            msg = in_data.decode('utf-8')

            if msg != '':
                print("От сервера :" , msg)
            else:
                print("Отключение клиента с msg = ''")
                client.close()
                break
        except ConnectionAbortedError:
            print("\nОтключение клиента ConnectionAbortedError")
            client.close()
            break

def send_to_server():
    while True:
        try:
            out_data = input()
            client.sendall(bytes(out_data, 'UTF-8'))
            print("Отпаравлено :" + str(out_data))
        except EOFError:
            print("\nОтключение клиента EOFError")
            client.close()
            break


if __name__ == '__main__':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))

    # поток для входящей информации
    input_thread = Thread(target=listen_server)
    # поток для исходящей информации
    output_thread = Thread(target=send_to_server)

    input_thread.start()
    output_thread.start()

    input_thread.join()
    output_thread.join()
