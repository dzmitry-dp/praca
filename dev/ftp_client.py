from ftplib import FTP_TLS
import os

from dev import action

HOST = "167.71.37.89"

CERTFILE = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        "./static/.ssl/cert.pem"))

def _check_public_key(cert: str):
    if os.path.exists(CERTFILE):
        print('Тут')
    else:
        print('Не тут')
        with open(CERTFILE, 'w') as file:
            file.write(cert)
    return CERTFILE

def _send_cmd_to_ftp_server(ftp) -> str:
    action.logger.info(f"ftp_client: _send_cmd_to_ftp_server")
    return ftp.sendcmd('pwd')

def connect_to_ftp(port: int, login: str, password: str, cert: str):
    action.logger.info(f"ftp_client: connect_to_ftp()")
    ftp = FTP_TLS()

    ftp.certfile = _check_public_key(cert)
    action.logger.info(f"DEBUG: Try connect to {HOST}:{port}")
    ftp.connect(HOST, port)
    action.logger.info(f"DEBUG: login = {login}, password = {password}")
    ftp.login(login, password)


    data = _send_cmd_to_ftp_server(ftp)
    action.logger.info(f"DEBUG: From server: {data}")

    ftp.quit()
    action.logger.info(f'DEBUG: Close connect')
