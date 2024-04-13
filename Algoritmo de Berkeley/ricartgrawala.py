import threading
import time
from queue import Queue

# Representación de un mensaje
class Message:
    def __init__(self, type, timestamp, sender):
        self.type = type  # Tipo de mensaje: 'request' o 'reply'
        self.timestamp = timestamp  # Marca de tiempo del mensaje
        self.sender = sender  # ID del proceso que envía el mensaje

# Representación de un proceso en el sistema distribuido
class DistributedProcess(threading.Thread):
    def __init__(self, pid, all_processes):
        super().__init__()
        self.pid = pid  # ID del proceso
        self.queue = Queue()  # Cola para mensajes de solicitud
        self.replies = 0  # Contador de respuestas recibidas
        self.all_processes = all_processes  # Referencia a todos los procesos
        self.requesting_critical_section = False
        self.timestamp = 0  # Marca de tiempo local

    def run(self):
        # Ejemplo de secuencia de acciones
        time.sleep(self.pid)  # Espera para simular desfase en las acciones
        self.request_access()  # Solicitar acceso a la región crítica
        time.sleep(1)  # Simular trabajo dentro de la región crítica
        self.release_access()  # Liberar la región crítica

    def request_access(self):
        self.timestamp += 1  # Actualizar marca de tiempo para la solicitud
        self.requesting_critical_section = True
        self.replies = 0
        message = Message('request', self.timestamp, self.pid)
        for process in self.all_processes:
            if process.pid != self.pid:
                process.receive_message(message)
        while self.replies < len(self.all_processes) - 1:
            pass  # Esperar hasta recibir todas las respuestas
        self.enter_critical_section()

    def enter_critical_section(self):
        current_time = time.strftime("%H:%M:%S.") + str(int((time.time() % 1) * 1000)).zfill(3)
        print(f'Proceso {self.pid} ({self.name}) entrando en la sección crítica a las {current_time}.')
        time.sleep(0.5)  # Simular trabajo en la sección crítica
        current_time = time.strftime("%H:%M:%S.") + str(int((time.time() % 1) * 1000)).zfill(3)
        print(f'Proceso {self.pid} ({self.name}) saliendo de la sección crítica a las {current_time}.')


    def release_access(self):
        self.requesting_critical_section = False
        while not self.queue.empty():
            message = self.queue.get()
            self.send_reply(message.sender)

    def receive_message(self, message):
        self.timestamp = max(self.timestamp, message.timestamp) + 1
        if message.type == 'request':
            if not self.requesting_critical_section or \
               (self.requesting_critical_section and
                (message.timestamp < self.timestamp or
                 (message.timestamp == self.timestamp and message.sender < self.pid))):
                self.send_reply(message.sender)
            else:
                self.queue.put(message)
        elif message.type == 'reply':
            self.replies += 1

    def send_reply(self, to_pid):
        for process in self.all_processes:
            if process.pid == to_pid:
                process.receive_message(Message('reply', self.timestamp, self.pid))

if __name__ == '__main__':
    num_processes = 3
    processes = [DistributedProcess(pid, []) for pid in range(num_processes)]
    for process in processes:
        process.all_processes = processes  # Asegurar que cada proceso conoce a los demás
    for process in processes:
        process.start()  # Iniciar todos los procesos
    for process in processes:
        process.join()  # Esperar a que todos los procesos terminen
