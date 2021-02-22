document.addEventListener('DOMContentLoaded', () => {
    sio = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    sio.emit('request_update', {'please': 'please'});

    counter = document.getElementById("server_amount");

    sio.on('send_update', (data) => {
        counter.innerHTML = data;
        setTimeout(() => { sio.emit('request_update', {'please': 'please'}) }, 5000);
    });
});