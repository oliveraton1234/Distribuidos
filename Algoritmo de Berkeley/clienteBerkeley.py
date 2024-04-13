import socket
import time

# Función para obtener el tiempo del servidor y ajustar el reloj local
def sync_clock(server_address):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Conectar al servidor
        s.connect(server_address)

        # Enviar el tiempo del cliente al servidor
        client_time = time.time()
        s.send(str(client_time).encode())
        print(f"Tiempo enviado al servidor {server_address}: {client_time}")

        # Recibir el tiempo del servidor
        server_time = float(s.recv(1024).decode())
        print(f"Tiempo recibido del servidor {server_address}: {server_time}")

        # Calcular la diferencia de tiempo y ajustar el reloj local
        time_diff = server_time - client_time
        local_time = time.time() + time_diff
        print(f"Reloj local ajustado: {local_time}")

# Dirección del servidor
server_address = ('127.0.0.1', 12345)

# Llamar a la función para sincronizar el reloj con el servidor
sync_clock(server_address)
