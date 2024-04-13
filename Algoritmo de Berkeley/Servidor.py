import socket
import threading
import time
from datetime import datetime

# Función para manejar cada cliente individualmente
def handle_client(conn, addr, client_times, server_initial_time):
    try:
        # Recibir el tiempo del cliente
        client_time = float(conn.recv(1024).decode())
        print(f"Tiempo recibido del cliente {addr}: {datetime.fromtimestamp(client_time).strftime('%Y-%m-%d %H:%M:%S.%f')}")

        # Añadir el tiempo del cliente a la lista
        client_times.append(client_time)

        # Esperar a que todos los clientes envíen su tiempo
        time.sleep(5)  # Este tiempo de espera es solo para fines de demostración

        # Calcular el tiempo ajustado y enviarlo de vuelta al cliente
        average_difference = calculate_average_difference(client_times, server_initial_time)
        adjusted_time = server_initial_time + average_difference
        conn.send(str(adjusted_time).encode())
        print(f"Tiempo ajustado enviado al cliente {addr}: {datetime.fromtimestamp(adjusted_time).strftime('%Y-%m-%d %H:%M:%S.%f')}")
    except Exception as e:
        print(f"Error al manejar al cliente {addr}: {e}")
    finally:
        conn.close()

# Función para calcular la diferencia promedio de tiempo
def calculate_average_difference(client_times, server_time):
    if not client_times:
        return 0
    total_difference = sum(client_times) - len(client_times) * server_time
    return total_difference / len(client_times)

def main():
    host = '175.1.53.167'
    port = 12345
    client_times = []

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print("Servidor iniciado, esperando conexiones...")

    server_initial_time = time.time()

    try:
        while True:
            conn, addr = server_socket.accept()
            print(f"Conexión establecida con {addr}")
            threading.Thread(target=handle_client, args=(conn, addr, client_times, server_initial_time)).start()
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
