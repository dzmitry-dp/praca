from ftplib import FTP_TLS
import os

from dev import action
import dev.config as config


def _check_public_key(cert: str):
    if not os.path.exists(config.CERTFILE):
        with open(config.CERTFILE, 'w') as file:
            file.write(cert)
    return config.CERTFILE

def connect_to_ftp(purpose: str, port: int, login: str, password: str, cert: str, path_to_employer_base: str):
    action.logger.info(f"ftp_client.py: connect_to_ftp()")

    def _send_cmd_to_ftp_server():
        action.logger.info(f"ftp_client.py: _send_cmd_to_ftp_server()")
        if purpose == 'update':
            # Скачивание базы данных работодателя с сервера
            with open(os.path.join(config.PATH_TO_EMPLOYER_DB, 'rockbit.db'), 'wb') as f:
                ftp.retrbinary(f'RETR {path_to_employer_base}', f.write)

    ftp = FTP_TLS()
    ftp.certfile = _check_public_key(cert)
    action.logger.info(f"DEBUG: FTP connect IP: {config.SERVER} PORT: {port}")
    ftp.connect(config.SERVER, port)
    ftp.login(login, password)
    ftp.prot_p()

    _send_cmd_to_ftp_server()
    ftp.quit()
