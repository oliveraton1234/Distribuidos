import socket

def sync_clock(server_address):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(server_address)

        # Enviar un mensaje inicial al servidor (contenido no relevante)
        s.sendall(b"Requesting server time")
        
        server_time = s.recv(1024).decode()
        print(f"Tiempo recibido del servidor: {server_time}")

server_address = ('175.1.53.86', 12345)
sync_clock(server_address)