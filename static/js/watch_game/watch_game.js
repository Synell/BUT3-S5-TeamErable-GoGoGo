const play_button = document.querySelector("#play");
const pause_button = document.querySelector("#pause");

const duration_time = document.querySelector("#duration-time");
const duration_slider = document.querySelector("#duration-slider");

const color = document.querySelector("#color").value;

const score_white = document.querySelector(".score.white");
const score_black = document.querySelector(".score.black");

const timer_white = document.querySelector("#timer-white");
const timer_black = document.querySelector("#timer-black");

let pause = true;

/**
 * Mettre à jour le temps
 */
function slider_send(time, new_time) {
    websocket.send(JSON.stringify({
        'type': 'get',
        'data': {
            'from': time,
            'to': new_time
        }
    }));
}

play_button.addEventListener("click", () => {
    play_button.classList.add("hidden");
    pause_button.classList.remove("hidden");
    pause = false;

    if (duration_slider.value === duration_slider.max) {
        duration_slider.value = 0;
        duration_time.innerText = "00:00:00";
        slider_send(parseInt(duration_slider.max, 10), 0);
    }
});

pause_button.addEventListener("click", () => {
    pause_button.classList.add("hidden");
    play_button.classList.remove("hidden");
    pause = true;
});



const base_url = window.location.hostname + ":" + window.location.port + "/";
const game_id = document.querySelector("#game-save-id").value;
const websocket = new WebSocket("ws://" + base_url + "game-save/" + game_id + "/");

/**
 * Envoie un message au serveur lorsqu'une touche est pressée
 * @param {string} event Event reçu par le serveur
 */
websocket.onmessage = function(event) {
    let raw_data = JSON.parse(event.data);
    let type = raw_data.type;
    let data = raw_data.data;

    switch(type) {
        case 'changes':
            receivedChanges(data); break;

        case 'timers':
            receivedTimers(data); break;

        case 'eaten-tiles':
            receivedEatenTiles(data); break;

        case 'error':
            notify('<p class="error">' + data + '</p>'); break;

        default:
            console.log("unknown message type: ", type); break;
    }
};

/**
 * Parse les données reçues par le serveur lors d'un coup
 * @param {string} stringData Données reçues par le serveur
 * @param {function} callback Fonction à appeler pour chaque coordonnée
*/
function parseReceivedChangesData(stringData, callback) {
    let list = stringData.split("\n");
    for (let i = 0; i < list.length; i++) {
        if (list[i] === "") continue;

        let coords = list[i].split(";");
        let x = parseInt(coords[0]);
        let y = parseInt(coords[1]);

        callback(x, y);
    }
}

/**
 * Message de coup reçu par le serveur
 * @param {string} data Données reçues par le serveur
 */
function receivedChanges(data) {
    let rm = data.r;
    let white = data.w;
    let black = data.b;

    parseReceivedChangesData(rm, (x, y) => {
        let stone = document.querySelector(`.stone[x="${x}"][y="${y}"]`);

        if (stone.classList.contains("white")) {
            stone.classList.remove("white");
        }
        else if (stone.classList.contains("black")) {
            stone.classList.remove("black");
        }
    });

    parseReceivedChangesData(white, (x, y) => {
        let stone = document.querySelector(`.stone[x="${x}"][y="${y}"]`);
        stone.classList.add("white");
    });

    parseReceivedChangesData(black, (x, y) => {
        let stone = document.querySelector(`.stone[x="${x}"][y="${y}"]`);
        stone.classList.add("black");
    });
}

/**
 * Message de timer reçu par le serveur
 * @param {string} data Données reçues par le serveur
 */
function receivedTimers(data) {
    timer_white.innerHTML = secondsToTime(data.w);
    timer_black.innerHTML = secondsToTime(data.b);
}

/**
 * Message de pierres mangées reçu par le serveur
 * @param {string} data Données reçues par le serveur
 */
function receivedEatenTiles(data) {
    score_white.innerHTML = data.w;
    score_black.innerHTML = data.b;
}
