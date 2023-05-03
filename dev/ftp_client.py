from ftplib import FTP_TLS
import socket
import os
import ssl

from dev import action
import dev.config as config

HOST = "167.71.37.89"

CERTFILE = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        "./static/.ssl/cert.pem"))

def _check_public_key(cert: str):
    if os.path.exists(CERTFILE):
        pass
    else:
        with open(CERTFILE, 'w') as file:
            file.write(cert)
    return CERTFILE

def connect_to_ftp(purpose: str, port: int, login: str, password: str, cert: str, path_to_employer_base: str):
    action.logger.info(f"ftp_client: connect_to_ftp()")

    def _send_cmd_to_ftp_server():
        action.logger.info(f"ftp_client: _send_cmd_to_ftp_server()")
        if purpose == 'update':
            # print(ftp.nlst())
            # Скачивание файла с сервера
            with open(config.PATH_TO_EMPLOYER_DB, 'wb') as f:
                ftp.retrbinary(f'RETR ./employer_base/rockbit.db', f.write)
    
    # Создаем объект FTP
    ftp = FTP_TLS()
    # Подключаемся к серверу
    ftp.certfile = _check_public_key(cert)
    # ftp.host = HOST
    # ftp.port = port
    ftp.connect(HOST, port)
    ftp.login(login, password)
    ftp.prot_p()

    _send_cmd_to_ftp_server()
    ftp.quit()
    