function get_data(counter){
    fetch('https://phonebotapi.herokuapp.com')
        .then(response => response.json())
        .then(data => counter.innerHTML = data);
    
    setTimeout(() => { get_data(counter) }, 1000);
}

document.addEventListener('DOMContentLoaded', () => {
    counter = document.getElementById("server_amount");
    get_data(counter);
});
