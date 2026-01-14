import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.IF_INET, socket.SOCK_STREAM)
        self.sever ="192.168.0.105"
        self.port = 5555
        self.addr =(self.sever, self.port)
        self.connect =()
    
    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode
        except:
            pass

