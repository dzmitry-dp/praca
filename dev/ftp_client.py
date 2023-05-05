from ftplib import FTP_TLS
import socket
import os
import ssl

from dev import action
import dev.config as config


def _check_public_key(cert: str):
    if os.path.exists(config.CERTFILE):
        pass
    else:
        with open(config.CERTFILE, 'w') as file:
            file.write(cert)
    return config.CERTFILE

def connect_to_ftp(purpose: str, port: int, login: str, password: str, cert: str, path_to_employer_base: str):
    action.logger.info(f"ftp_client: connect_to_ftp()")

    def _send_cmd_to_ftp_server():
        action.logger.info(f"ftp_client: _send_cmd_to_ftp_server()")
        if purpose == 'update':
            # Скачивание файла с сервера
            with open(config.PATH_TO_EMPLOYER_DB, 'wb') as f:
                ftp.retrbinary(f'RETR ./employer_base/rockbit.db', f.write)
    
    ftp = FTP_TLS()
    ftp.certfile = _check_public_key(cert)
    ftp.connect(config.SERVER, port)
    ftp.login(login, password)
    ftp.prot_p()

    _send_cmd_to_ftp_server()
    ftp.quit()
    