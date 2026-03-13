import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.player_id = self.connect_to_server()

    def get_player_id(self):
        return self.player_id

    def connect_to_server(self):
        try:
            self.client.connect(self.addr)
            # Server sends back our player ID (0 or 1)
            data = self.client.recv(4096)
            return pickle.loads(data)
        except Exception as e:
            print("Connection error:", e)
            return None

    def send(self, data):
        """Send our state and receive opponent's state."""
        try:
            self.client.send(pickle.dumps(data))
            response = self.client.recv(4096)
            return pickle.loads(response)
        except socket.error as e:
            print("Send error:", e)
            return None

    def wait_for_ready(self):
        """Wait for server to signal that both players are connected."""
        try:
            data = self.client.recv(4096)
            signal = pickle.loads(data)
            return signal == "ready"
        except Exception as e:
            print("Wait error:", e)
            return False
