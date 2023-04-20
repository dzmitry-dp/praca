from ftplib import FTP_TLS
# from OpenSSL import SSL
import os

HOST = "167.71.37.89"
PORT = 1488

# ftp_dir = '.'
CERTFILE = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        "./.ssl/cert.pem"))

if __name__ == '__main__':
    ftps = FTP_TLS()
    ftps.certfile = CERTFILE
    ftps.connect(HOST, PORT)

    ftps.login('user', '12345')

    # ftps.cwd(ftp_dir)

    data = ftps.sendcmd('pwd')
    print(data)

    ftps.quit()
