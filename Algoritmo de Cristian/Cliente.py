import socket
import time
from datetime import datetime

def sync_clock(server_address):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect(server_address)

            # Marcar el tiempo de envío de la solicitud
            send_time = time.time()
            s.send(b'request')

            # Recibir el tiempo del servidor y marcar el tiempo de recepción
            server_time = float(s.recv(1024).decode())
            receive_time = time.time()

            # Calcular el retardo de ida y vuelta (RTT) y el tiempo ajustado
            rtt = receive_time - send_time
            adjusted_time = server_time + rtt / 2

            # Convertir a formato legible
            readable_send_time = datetime.fromtimestamp(send_time).strftime('%Y-%m-%d %H:%M:%S.%f')
            readable_server_time = datetime.fromtimestamp(server_time).strftime('%Y-%m-%d %H:%M:%S.%f')
            readable_adjusted_time = datetime.fromtimestamp(adjusted_time).strftime('%Y-%m-%d %H:%M:%S.%f')

            print(f"Tiempo local enviado: {readable_send_time}")
            print(f"Tiempo recibido del servidor: {readable_server_time}")
            print(f"Tiempo ajustado (local): {readable_adjusted_time}")
        except Exception as e:
            print(f"Error: {e}")

# Dirección del servidor
server_address = ('127.0.0.1', 12345)

# Sincronizar el reloj con el servidor
sync_clock(server_address)
