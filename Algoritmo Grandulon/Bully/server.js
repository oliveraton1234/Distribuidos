const http = require('http');
const socketio = require('socket.io');

const server = http.createServer((req, res) => {
    res.end('Bully Algorithm Server');
});

const io = socketio(server);
const clients = [];
const clientStrengths = {};

io.on('connection', (socket) => {
    console.log(`Cliente conectado: ${socket.id}`);
    const strength = Math.random();
    clients.push(socket);
    clientStrengths[socket.id] = strength;

    io.emit('message', `Nuevo cliente conectado: ${socket.id}, fuerza: ${strength}`);
    performLeaderElection();  // Elección de líder cada vez que un nuevo cliente se conecta

    socket.on('disconnect', () => {
        console.log(`Cliente desconectado: ${socket.id}`);
        const index = clients.indexOf(socket);
        if (index > -1) {
            clients.splice(index, 1);
            delete clientStrengths[socket.id];
            io.emit('message', `Cliente ${socket.id} ha caído. Reorganizando...`);
            performLeaderElection();
        }
    });

    socket.on('election', () => {
        performLeaderElection();
    });
});

function performLeaderElection() {
    const strongest = Object.keys(clientStrengths).reduce((a, b) => clientStrengths[a] > clientStrengths[b] ? a : b);
    io.emit('message', `Nuevo líder elegido: ${strongest}`);
    clients.forEach(client => {
        if (client.id === strongest) {
            client.emit('leader', 'Eres el nuevo líder');
        }
    });
}

const PORT = 3000;
server.listen(PORT, () => {
    console.log(`Servidor escuchando en el puerto ${PORT}`);
});
