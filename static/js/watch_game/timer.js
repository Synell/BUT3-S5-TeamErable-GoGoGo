/**
 * Met à jour le temps
 * @param {HTMLElement} countdownElement Elemennt du temps
 */
function updateCountdown(countdownElement, value) {
    // Récupérer la valeur du temps actuel au format "hh:mm:ss"
    var currentTime = countdownElement.innerText;
    var timeArray = currentTime.split(":");
    var hours = parseInt(timeArray[0], 10);
    var minutes = parseInt(timeArray[1], 10);
    var seconds = parseInt(timeArray[2], 10);

    // Ajouter la valeur au temps actuel
    seconds += value;
    if (seconds < 0) {
        minutes -= 1;
        seconds = 60 + seconds;
    }
    else if (seconds > 59) {
        minutes += 1;
        seconds = seconds - 60;
    }

    if (minutes < 0) {
        hours -= 1;
        minutes = 60 + minutes;
    }
    else if (minutes > 59) {
        hours += 1;
        minutes = minutes - 60;
    }

    // Mettre à jour l'élément avec la nouvelle valeur
    countdownElement.innerText = formatTime(hours) + ":" + formatTime(minutes) + ":" + formatTime(seconds);

    return seconds <= 0 && minutes <= 0 && hours <= 0;
}

/**
 * Convertir les secondes en temps
 * @param {number} seconds Le nombre de secondes
 * @returns {string} Le temps au format "hh:mm:ss"
 */
function secondsToTime(seconds) {
    var hours = Math.floor(seconds / 3600);
    var minutes = Math.floor((seconds - (hours * 3600)) / 60);
    seconds = seconds - (hours * 3600) - (minutes * 60);

    return formatTime(hours) + ":" + formatTime(minutes) + ":" + formatTime(seconds);
}

/**
 * Convertir le temps en secondes
 * @param {string} time Le temps au format "hh:mm:ss"
 * @returns {number} Le nombre de secondes
 */
function timeToSeconds(time) {
    var timeArray = time.split(":");
    var hours = parseInt(timeArray[0], 10);
    var minutes = parseInt(timeArray[1], 10);
    var seconds = parseInt(timeArray[2], 10);

    return hours * 3600 + minutes * 60 + seconds;
}

/**
 * Formater le temps
 * @param {number} time Le chiffre à formater
 * @returns {string} Le temps avec un 0 devant le chiffre
 */
function formatTime(time) {
    return time < 10 ? "0" + time : time;
}

// Exécuter la fonction updateCountdown toutes les secondes
setInterval( function() {
    if (parseInt(duration_slider.value, 10) >= parseInt(duration_slider.max, 10)) {
        pause_button.classList.add("hidden");
        play_button.classList.remove("hidden");
        pause = true;
    }

    if (pause === false) {
        updateCountdown(duration_time, 1);

        let dslider = parseInt(duration_slider.value, 10);

        websocket.send(JSON.stringify({
            'type': 'get',
            'data': {
                'from': dslider,
                'to': dslider + 1
            }
        }));

        duration_slider.value = dslider + 1;
    }
}, 1000);

// Mettre à jour le temps en fonction de la valeur du slider
duration_slider.addEventListener("input", () => {
    let time = timeToSeconds(duration_time.innerText);
    let new_time = parseInt(duration_slider.value, 10);
    duration_time.innerText = secondsToTime(new_time);

    slider_send(time, new_time);
});
