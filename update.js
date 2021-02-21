document.addEventListener('DOMContentLoaded', () => {
    console.log('banana')
    sio = io.connect('http://localhost:5000');
    sio.emit('request_update');

    counter = document.getElementById("server_amount");
    //counter.innerHTML = 15;

    sio.on('send_update', (data) => {
        console.log(data)
        counter.innerHTML = data['guild_amount'];
        setTimeout(() => { sio.emit('request_update') }, 5000);
    });
});