
const base_url = window.location.hostname + ":" + window.location.port + "/";
const game_id = document.querySelector("#game-id").value;
const websocket = new WebSocket("ws://" + base_url + "game/" + game_id + "/");
const player_color = document.querySelector("#player-color").value;
let game_ended = document.querySelector("#game-ended").value === "True" ? true : false;
let has_second_player = document.querySelector("#has-second-player").value === "True" ? true : false;

const pause_count_element = document.querySelector("#span-pause-count");

const resume_timer_element = document.querySelector("#span-resume-timer");
const resume_button = document.querySelector("#resume-button");

const start_timer_element = document.querySelector("#span-start-timer");
const start_button = document.querySelector("#start-div");
const start_count_element = document.querySelector("#span-start-count");

let game_is_paused = parseInt(document.querySelector("#game-paused").value, 10);


/**
 * Envoie un message de connexion au serveur
 * @param {string} event Event reçu par le serveur
 */
websocket.onopen = function(event) {
    websocket.send(JSON.stringify({
        'type': 'connect',
        'data': null
    }));
}

/**
 * Envoie un message de déconnexion au serveur
 * @param {string} event Event reçu par le serveur
 */
websocket.onclose = function(event) {
    websocket.send(JSON.stringify({
        'type': 'disconnect',
        'data': null
    }));
}

/**
 * Envoie un message au serveur lorsqu'une touche est pressée
 * @param {string} event Event reçu par le serveur
 */
websocket.onmessage = function(event) {
    let raw_data = JSON.parse(event.data);
    let type = raw_data.type;
    let data = raw_data.data;

    switch(type) {
        case 'connect':
            receivedConnect(data); break;

        case 'disconnect':
            break; // Ne fait rien pour l'instant, mais on pourrait afficher une notification

        case 'play':
            receivedPlay(data); break;

        case 'can-play':
            receivedCanPlay(data); break;

        case 'eaten-tiles':
            receivedEatenTiles(data); break;

        case 'timers':
            receivedTimers(data); break;

        case 'end-game':
            receivedEndGame(data); break;

        case 'pause':
            receivedPause(data); break;

        case 'resume':
            receivedResume(data); break;

        case 'pause-timer':
            receivedPauseTimer(data); break;

        case 'start':
            receivedStart(data); break;

        case 'error':
            notify('<p class="error">' + data + '</p>'); break;

        default:
            console.log("unknown message type: ", type); break;
    }
}

/**
 * Message de connexion reçu par le serveur
 * @param {string} data Données reçues par le serveur
 */
function receivedConnect(data) {
    has_second_player = true;

    let user_id = data.id;
    let color = data.color;

    let formData = new FormData();
    formData.append("game-id", game_id);
    formData.append("user-id", user_id);
    
    let csrf_token = document.querySelector("input[name=csrfmiddlewaretoken]").value;

    var request = new XMLHttpRequest();
    request.open('POST', '/game-view-player');
    request.setRequestHeader('X-CSRFToken', csrf_token);
    request.onload = function() {
        if (request.status === 200) {
            document.querySelector("#container-" + color + "-player").innerHTML = request.responseText;
        }
        else {
            console.log("error: ", request.responseText);
        }
    }
    request.send(formData);
}

/**
 * Parse les données reçues par le serveur lors d'un coup
 * @param {string} stringData Données reçues par le serveur
 * @param {function} callback Fonction à appeler pour chaque coordonnée
*/
function parseReceivedPlayData(stringData, callback) {
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
function receivedPlay(data) {
    let changes = JSON.parse(data);

    let rm = changes.r;
    let white = changes.w;
    let black = changes.b;

    parseReceivedPlayData(rm, (x, y) => {
        let stone = document.querySelector(`.stone[x="${x}"][y="${y}"]`);

        if (stone.classList.contains("white")) {
            stone.classList.remove("white");
        }
        else if (stone.classList.contains("black")) {
            stone.classList.remove("black");
        }
    });

    parseReceivedPlayData(white, (x, y) => {
        let stone = document.querySelector(`.stone[x="${x}"][y="${y}"]`);
        stone.classList.add("white");
    });

    parseReceivedPlayData(black, (x, y) => {
        let stone = document.querySelector(`.stone[x="${x}"][y="${y}"]`);
        stone.classList.add("black");
    });
}

/**
 * Message de jeu reçu par le serveur
 * @param {string} data Données reçues par le serveur
 */
function receivedCanPlay(data) {
    if (data === true) {
        board.classList.add("can-play");
        action_buttons.classList.remove("hidden");
    }
    else {
        board.classList.remove("can-play");
        action_buttons.classList.add("hidden");
    }
}

/**
 * Message de pierres mangées reçu par le serveur
 * @param {string} data Données reçues par le serveur
 */
function receivedEatenTiles(data) {
    let eaten = JSON.parse(data);

    let score_white = document.querySelector(".score.white");
    let score_black = document.querySelector(".score.black");

    score_white.innerHTML = eaten.w;
    score_black.innerHTML = eaten.b;
}

/**
 * Message de timers reçu par le serveur
 * @param {string} data Données reçues par le serveur
 */
function receivedTimers(data) {
    let timers = JSON.parse(data);

    let timer_white = document.querySelector("#timer-white");
    let timer_black = document.querySelector("#timer-black");

    timer_white.innerHTML = timers.w;
    timer_black.innerHTML = timers.b;
}

/**
 * Message de fin de partie reçu par le serveur
 * @param {string} data Données reçues par le serveur
 */
function receivedEndGame(data) {
    game_ended = true;

    let parsed_data = JSON.parse(data);

    let winner = parsed_data.winner;
    let points = parsed_data.points;

    let end_game_modal = document.querySelector("#band-win");

    let winner_text = end_game_modal.querySelector("#band-win-big-text");
    let points_text = end_game_modal.querySelector("#band-win-small-text");

    if (winner === "w") {
        winner_text.innerHTML = `Les blancs (${points[winner].username}) ont gagné la partie !`;
        points_text.innerHTML = `${points.w.count} (${points.w.username}) vs ${points.b.count} (${points.b.username})`;
    }
    else if (winner === "b") {
        winner_text.innerHTML = `Les noirs (${points[winner].username}) ont gagné la partie !`;
        points_text.innerHTML = `${points.b.count} (${points.b.username}) vs ${points.w.count} (${points.w.username})`;
    }
    else {
        winner_text.innerHTML = "Égalité !";
        points_text.innerHTML = `${points.w.count} (${points.w.username}) vs ${points.b.count} (${points.b.username})`;
    }

    end_game_modal.classList.remove("hidden");
}

/**
 * Message de pause reçu par le serveur
 * @param {string} data Données reçues par le serveur
 */
function receivedPause(data) {
    pause_count_element.innerHTML = data.pause_count.toString();
    game_is_paused = data.is_paused;

    if (data.is_paused) {
        let element = document.querySelector("#band-pause");
        if (element.classList.contains("hidden")) element.classList.remove("hidden");
    }
}

/**
 * Message de reprise reçu par le serveur
 * @param {string} data Données reçues par le serveur
 */
function receivedResume(data) {
    pause_count_element.innerHTML = data.pause_count.toString();
    game_is_paused = data.is_paused;

    if (!data.is_paused) {
        let element = document.querySelector("#band-pause");
        if (!element.classList.contains("hidden")) element.classList.add("hidden");
    }
}


/**
 * Message de pause du timer reçu par le serveur
 * @param {string} data Données reçues par le serveur
 */
function receivedPauseTimer(data) {
    resume_timer_element.innerHTML = data.timer;
    if (!resume_button.classList.contains("hidden")) {
        resume_button.classList.add("hidden");
    }
}


/**
 * Message de début de partie reçu par le serveur
 * @param {string} data Données reçues par le serveur
 */
function receivedStart(data) {
    start_count_element.innerHTML = data.start_count.toString();
    game_is_paused = data.is_paused;

    if (!data.is_paused) {
        let element = document.querySelector("#band-start");
        if (!element.classList.contains("hidden")) element.classList.add("hidden");
    }
}


// Place une pierre sur le plateau si on clique dessus et qu'on peut jouer
document.querySelectorAll(".stone").forEach((element) => {
    element.addEventListener("click", () => {
        play(element);
    });
});

const board = document.querySelector(".board");
const action_buttons = document.querySelector("#action-buttons");

/**
 * Renvoie si on peut jouer ou non
 * @returns {boolean} Si on peut jouer ou non
 */
function getCanPlay() {
    return board.classList.contains("can-play");
}

/**
 * Renvoie la couleur de l'adversaire
 * @returns {string} Couleur de l'adversaire
 */
function getOpponentColor() {
    return player_color === "white" ? "black" : "white";
}

/**
 * Joue un coup
 * @param {HTMLElement} element Élément sur lequel on a cliqué
 */
function play(element) {
    if (getCanPlay()) {
        websocket.send(JSON.stringify({
            'type': 'play',
            'data': element.attributes.x.value + ";" + element.attributes.y.value
        }));
    }
}

/**
 * Envoie un message pour passer son tour
 */
function skip() {
    websocket.send(JSON.stringify({
        'type': 'skip',
        'data': null
    }));
}

/**
 * Envoie un message pour abandonner
 */
function giveUp() {
    websocket.send(JSON.stringify({
        'type': 'give-up',
        'data': null
    }));
}

/**
 * Envoie un message demander à mettre en pause
 */
function askPause() {
    websocket.send(JSON.stringify({
        'type': 'pause',
        'data': null
    }));
}

/**
 * Envoie un message demander à reprendre
 */
function askResume() {
    websocket.send(JSON.stringify({
        'type': 'resume',
        'data': null
    }));
}

/**
 * Envoie un message demander à commencer
 */
function askStart() {
    websocket.send(JSON.stringify({
        'type': 'start',
        'data': null
    }));
}

document.querySelector("#skip-button").addEventListener("click", skip);
document.querySelector("#give-up-button").addEventListener("click", giveUp);

try { document.querySelector("#pause-button").addEventListener("click", askPause); }
catch (e) { }

document.querySelector("#resume-button").addEventListener("click", askResume);
document.querySelector("#start-button").addEventListener("click", askStart);


/**
 * Envoie un message pour update l'état de la partie
 */
function checkState() {
    websocket.send(JSON.stringify({
        'type': 'check-state',
        'data': null
    }));
}



const code = document.querySelector("#code");

/**
 * Affiche ou cache le code
 */
function toggleCodeVisibility() {
    let checked = document.querySelector("#show-code").querySelector("input[type=checkbox]").checked;
    if (checked) code.classList.remove("opacity-0");
    else code.classList.add("opacity-0");
}
