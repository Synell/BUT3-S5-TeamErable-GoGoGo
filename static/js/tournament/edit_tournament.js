document.body.addEventListener("htmx:afterRequest", function(event) {
    if (
        !(
            (event.detail.xhr.responseURL.startsWith(window.location.origin + "/edit-tournament"))
        )
    ) return;
    document.querySelector('form input[type="submit"]').disabled = true;
    if (event.detail.xhr.status == 200) {
        setTimeout(function() {
            window.location.href = event.detail.xhr.responseText;
        }, 1000);
    }
    else {
        notify(event.detail.xhr.responseText);
        document.querySelector('form input[type="submit"]').disabled = false;
    }
});



setTimeout(function() {
    var mindate = document.getElementById("start-date");
    mindate.dispatchEvent(new Event('change'));
}, 50);



// Récupérer la case à cocher et le div
var handicap = document.getElementById('handicap-form');

/**
 * Ajouter un routeur d'événement pour la case à cocher
 */
function toggleHandicap() {

    // Inverser l'état actif du switch button
    let switchbutton = document.getElementById('tournament-is-handicap').querySelector('input[type="checkbox"]');

    // Si le switch button est activé, afficher le div, sinon le masquer
    handicap.hidden = !switchbutton.checked;
};