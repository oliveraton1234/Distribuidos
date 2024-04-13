import socket
import time

# Función para calcular el tiempo promedio
def calculate_average_time(times):
    return sum(times) / len(times)

# Función para manejar las solicitudes de los clientes y sincronizar los relojes
def handle_client(conn, addr, node_times):
    # Recibir el tiempo del cliente
    client_time = float(conn.recv(1024).decode())
    print(f"Tiempo recibido del cliente {addr}: {client_time}")

    # Agregar el tiempo del cliente a la lista
    node_times.append(client_time)

    # Enviar el tiempo del servidor al cliente
    server_time = time.time()
    conn.send(str(server_time).encode())
    print(f"Tiempo enviado al cliente {addr}: {server_time}")

    # Cerrar la conexión
    conn.close()

# Función principal del servidor
def main():
    host = '175.1.53.167'
    port = 12345

    # Crear un socket TCP/IP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Enlace del socket al puerto
        s.bind((host, port))
        print("Servidor iniciado.")

        # Esperar conexiones entrantes
        s.listen()
        node_times = []

        while True:
            conn, addr = s.accept()
            print(f"Conexión establecida con {addr}")
            # Manejar la solicitud del cliente en un hilo separado
            handle_client(conn, addr, node_times)

            # Sincronizar los relojes utilizando el algoritmo de Berkeley
            average_time = calculate_average_time(node_times)
            adjusted_times = [time + (average_time - time) for time in node_times]
            print("Tiempos sincronizados:", adjusted_times)

# Llamar a la función principal del servidor
if __name__ == "__main__":
    main()
