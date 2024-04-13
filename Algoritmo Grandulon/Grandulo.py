

import socket
import threading
import time

class BullyNode:
    def __init__(self, id, ports):
        self.id = id
        self.ports = ports  # Dictionary of all node IDs to their ports
        self.coordinator = max(self.ports.keys())
        self.host = '175.1.46.164'
        self.port = self.ports[self.id]
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.alive = True

    def listen(self):
        self.socket.listen(5)
        print(f"Node {self.id} listening on port {self.port}")
        while self.alive:
            conn, addr = self.socket.accept()
            threading.Thread(target=self.handle_message, args=(conn,)).start()

    def handle_message(self, conn):
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode()
            if message.startswith('ELECTION'):
                sender_id = int(message.split()[-1])
                self.respond_to_election(sender_id)
            elif message.startswith('COORDINATOR'):
                new_coordinator = int(message.split()[-1])
                self.update_coordinator(new_coordinator)
        conn.close()

    def respond_to_election(self, sender_id):
        if self.id > sender_id:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, self.ports[sender_id]))
                s.sendall(f"OK {self.id}".encode())

    def update_coordinator(self, new_coordinator):
        self.coordinator = new_coordinator
        print(f"Node {self.id} acknowledges new coordinator {self.coordinator}")

    def initiate_election(self):
        responses = []
        for nid in self.ports:
            if nid > self.id:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((self.host, self.ports[nid]))
                        s.sendall(f"ELECTION from {self.id}".encode())
                        responses.append(nid)
                except ConnectionRefusedError:
                    continue
        if not responses:  # No responses, I'm the highest or only node
            self.announce_coordinator()

    def announce_coordinator(self):
        for nid in self.ports:
            if nid != self.id:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((self.host, self.ports[nid]))
                        s.sendall(f"COORDINATOR {self.id}".encode())
                except ConnectionRefusedError:
                    continue
        self.coordinator = self.id
        print(f"Node {self.id} is now the coordinator.")

def get_unique_id():
    # Generate a unique ID based on current timestamp
    return int(time.time() * 1000)

if __name__ == "__main__":
    # Example of starting a node
    node_ports = {1: 65432, 2: 65433, 3: 65434}
    node_id = get_unique_id()  # Unique ID for each node
    node = BullyNode(node_id, node_ports)
    threading.Thread(target=node.listen).start()
    time.sleep(2)  # Give time for server setup
    if node_id == min(node_ports.keys()):  # Example of initiating election for the node with the lowest ID
        node.initiate_election()
