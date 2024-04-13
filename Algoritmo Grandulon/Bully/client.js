const readline = require('readline');
const io = require('socket.io-client');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

const serverIP = '175.1.42.45';  // Cambia esto con la IP de tu servidor

const socket = io.connect(`http://${serverIP}:3000`);

socket.on('connect', () => {
    console.log('Conectado al servidor.');
});

socket.on('message', (data) => {
    console.log('Mensaje del servidor:', data);
});

socket.on('token', (message) => {
    console.log(message);
    // Simula procesamiento o alguna acción
    setTimeout(() => {
        socket.emit('token', 'Token procesado');
    }, 1000);
});

socket.on('disconnect', () => {
    console.log('Desconectado del servidor.');
    rl.close();
});

rl.on('close', () => {
    process.exit(0);
});
