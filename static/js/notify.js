// Temps d'affichage de la notification
const notif_time = 5000;

/**
 * Affiche une notification sur le haut de la page
 * @param {string} message Le message a afficher
 */
function notify(message) {
    var notifyElement = document.querySelector(".notify ul");
    var notif = document.createElement("li");
    notifyElement.appendChild(notif);
    notif.innerHTML = message;
    while (notif.children.length > 1) { // Pour une raison inconnue, le innerHTML ajoute 2 enfants au lieu d'un seul
        notif.removeChild(notif.children[1]);
    }

    setTimeout(function(){
        notif.remove();
    }, notif_time);
}
