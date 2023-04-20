import socketserver


# LOCALHOST = "159.223.25.102"
# New-NetFirewallRule -DisplayName "Allow Port 1489" -Direction Inbound -Protocol TCP -LocalPort 1489 -Action Allow
LOCALHOST = ''
PORT = 1489

class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class EventsHandler(socketserver.BaseRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_ip = None
        self.client_port = None

    def handle(self):
        data = self.request.recv(4096).strip()
        
        self.client_ip = self.client_address[0]
        self.client_port = self.client_address[1]

        print(f'Address: {self.client_address}')
        print(f'Data: {data.decode("utf-8")}')


if __name__ == '__main__':
    with ThreadingTCPServer((LOCALHOST, PORT), EventsHandler) as server:
        server.serve_forever()