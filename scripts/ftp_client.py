# запускай из /Praca командой python ./scripts/ftp_client.py

from ftplib import FTP_TLS
import os

HOST = "167.71.37.89"
PORT = 1488

# ftp_dir = '.'
CERTFILE = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        "../static/.ssl/cert.pem"))

def send_cmd() -> str:
    return ftps.sendcmd('pwd')

if __name__ == '__main__':
    ftps = FTP_TLS()

    ftps.certfile = CERTFILE
    ftps.connect(HOST, PORT)
    ftps.login('user', '12345')

    data = send_cmd()
    print(data)

    ftps.quit()
