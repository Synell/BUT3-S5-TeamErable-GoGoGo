htmx.config.useTemplateFragments = true;

/**
 * Fonction pour importer un jeu
 */
function importGame() {
    var fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = '.json';

    // Ajoutez un événement onchange pour déclencher l'envoi du fichier une fois sélectionné
    fileInput.addEventListener('change', function () {
        uploadFile(fileInput.files[0]);
    });

    // Cliquez sur le champ de fichier virtuel
    fileInput.click();
}

/**
 * Fonction pour importer un jeu
 * @param {File} file Fichier importé
 */
function uploadFile(file) {
    var formData = new FormData();
    let csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    formData.append('json_file', file);

    // Effectuez une requête Ajax vers le serveur avec le fichier
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/import-game', true);
    xhr.setRequestHeader('X-CSRFToken', csrf_token);
    xhr.onload = function () {
        if (xhr.status === 200) {
            // Succès de la requête, effectuez des actions supplémentaires si nécessaire
            notify(xhr.responseText);
            htmx.trigger('body', 'reload');
        } else {
            // Gestion des erreurs
            notify(xhr.responseText);
        }
    };

    // Envoyez la requête avec le formulaire de données contenant le fichier
    xhr.send(formData);
}

