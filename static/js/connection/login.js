/**
 * Fonction de validation du formulaire
 * 
 * @returns {boolean} Renvoie si le formulaire est valide
 */
function validateForm() {
    document.querySelector('input[type="submit"]').disabled = true;

    var formData = new FormData();
    formData.append('username', document.getElementById('username').value);
    formData.append('password', document.getElementById('password').value);

    var csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    var request = new XMLHttpRequest();
    request.open('POST', '/login');
    request.setRequestHeader('X-CSRFToken', csrf_token);
    request.onload = function() {
        if (request.status === 200) {
            window.location.href = '/';
        }
        else {
            notify(request.responseText);
            document.querySelector('input[type="submit"]').disabled = false;
        }
    };
    request.send(formData);

    return false;
}
