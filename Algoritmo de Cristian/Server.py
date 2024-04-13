import socket
import time
from datetime import datetime

def handle_client(conn, addr):
    with conn:
        # Recibir solicitud del cliente (el contenido específico no es relevante)
        _ = conn.recv(1024)
        
        # Registrar el tiempo de recepción de la solicitud y convertirlo a formato legible
        receive_time = time.time()
        readable_receive_time = datetime.fromtimestamp(receive_time).strftime('%Y-%m-%d %H:%M:%S:%f')
        print(f"Tiempo de recepción de solicitud de {addr}: {readable_receive_time}")

        # Enviar el tiempo actual del servidor al cliente
        server_time = time.time()
        readable_server_time = datetime.fromtimestamp(server_time).strftime('%Y-%m-%d %H:%M:%S:%f')
        conn.send(str(server_time).encode())
        print(f"Tiempo enviado al cliente {addr}: {readable_server_time}")

def main():
    host = '175.1.53.167'
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        print("Servidor iniciado, esperando conexiones...")
        s.listen()

        while True:
            conn, addr = s.accept()
            print(f"Conexión establecida con {addr}")
            handle_client(conn, addr)

if __name__ == "__main__":
    main()
