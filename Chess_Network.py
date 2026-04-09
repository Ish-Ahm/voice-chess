import socket
import pickle

class Network:
    def __init__(self, is_host, ip="0.0.0.0", port=5555):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None
        self.is_host = is_host

        if is_host:
            self.sock.bind((ip, port))
            self.sock.listen(1)
            print("waiting for connection...")
            self.conn, addr = self.sock.accept()
            print("connected to", addr)
        else:
            self.sock.connect((ip, port))
            self.conn = self.sock

    def send(self, data):
        self.conn.sendall(pickle.dumps(data))

    def receive(self):
        return pickle.loads(self.conn.recv(4096))