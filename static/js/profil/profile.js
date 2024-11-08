/**
 * Lire l'URL de l'image
 * @param {*} input 
 */
function readURL(input) {
    if (input.files && input.files[0]) {
        var csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

        var formData = new FormData();
        formData.append('pfp', input.files[0]);
        var request = new XMLHttpRequest();
        request.open('POST', '/change-pfp');
        request.setRequestHeader('X-CSRFToken', csrf_token);
        request.onload = function() {
            notify(request.responseText);

            if (request.status == 200) {
                var reader = new FileReader();
                reader.onload = function(e) {
                    document.querySelector('.profile-pic').setAttribute('src', e.target.result);
                }
                reader.readAsDataURL(input.files[0]);
            }
        }
        request.send(formData);
    }
}

document.querySelector(".file-upload").addEventListener('change', function(){
    readURL(this);
});

document.querySelector(".upload-button").addEventListener('click', function() {
    document.querySelector(".file-upload").click();
});


/*
document.querySelectorAll(".sidebar-link").forEach(function(element) {
    element.addEventListener('click', function(event) {
        var links = document.querySelectorAll(".sidebar-link");
        links.forEach(element => {
            element.classList.remove("active");
        });
    
        var sections = document.querySelectorAll("section");
        sections.forEach(element => {
            element.classList.remove("active");
        });
    
        event.target.classList.toggle("active");
        document.querySelector(event.target.getAttribute("activate")).classList.toggle("active");
    });
});
*/


document.querySelector("#change-pwd").addEventListener('submit', function(event) {
    event.preventDefault();
    document.querySelector('form#change-pwd input[type="submit"]').disabled = true;
    var csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    var formData = new FormData();
    formData.append('old-pwd', document.querySelector('input[name="old-pwd"]').value);
    formData.append('new-pwd', document.querySelector('input[name="new-pwd"]').value);
    formData.append('new-pwd-confirm', document.querySelector('input[name="new-pwd-confirm"]').value);
    var request = new XMLHttpRequest();
    request.open('POST', '/change-pwd');
    request.setRequestHeader('X-CSRFToken', csrf_token);
    request.onload = function() {
        if (request.status == 400) {
            notify(request.responseText);
            document.querySelector('form#change-pwd input[type="submit"]').disabled = false;
        } else if (request.status == 200) {
            notify(request.responseText);
            setTimeout(function() {
                window.location.reload();
            }, 1000);
        }
    }
    request.send(formData);
});




document.querySelector("#search-input").addEventListener('keyup', function(event) {
    var formData = new FormData();
    formData.append('username', event.target.value);

    var csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    var request = new XMLHttpRequest();
    request.open('POST', '/search-notfriend-user');
    request.setRequestHeader('X-CSRFToken', csrf_token);
    request.onload = function() {
        if (request.status == 200) {
            document.querySelector("#user-datalist").innerHTML = request.responseText;
            htmx.process(document.querySelector("#user-datalist"));
        }
    }
    request.send(formData);
});



document.body.addEventListener("htmx:afterRequest", function(event) {
    setTimeout(function() {
        if (
            !(
                (event.detail.xhr.responseURL.startsWith(window.location.origin + "/add-friend")) ||
                (event.detail.xhr.responseURL.startsWith(window.location.origin + "/delete-friend"))
            )
        ) return;
        notify(event.detail.xhr.responseText);

        document.querySelector("#search-input").dispatchEvent(new KeyboardEvent('keyup', {key: 'a'}));

        var formData = new FormData();
        var csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

        var request = new XMLHttpRequest();
        request.open('GET', '/friend-list');
        request.setRequestHeader('X-CSRFToken', csrf_token);
        request.onload = function() {
            if (request.status == 200) {
                document.querySelector("#friends-list").innerHTML = request.responseText;
                htmx.process(document.querySelector("#friends-list"));
            }
        }
        request.send(formData);
    }, 100);
});



document.querySelector("#delete-account").addEventListener('submit', function(event) {
    event.preventDefault();
    document.querySelector('form#delete-account input[type="submit"]').disabled = true;
    var csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    var formData = new FormData();
    formData.append('password', document.querySelector('input[name="password"]').value);
    var request = new XMLHttpRequest();
    request.open('POST', '/delete-account');
    request.setRequestHeader('X-CSRFToken', csrf_token);
    request.onload = function() {
        if (request.status == 400) {
            notify(request.responseText);
            document.querySelector('form#delete-account input[type="submit"]').disabled = false;
        } else if (request.status == 200) {
            notify(request.responseText);
            setTimeout(function() {
                window.location.href = "/login";
            }, 1000);
        }
    }
    request.send(formData);
});


document.querySelector("#change-user-info").addEventListener('submit', function(event) {
    event.preventDefault();
    document.querySelector('form#change-user-info input[type="submit"]').disabled = true;

    var csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    var formData = new FormData();
    formData.append('username', document.querySelector('input[name="username"]').value);
    formData.append('email', document.querySelector('input[name="email"]').value);

    var request = new XMLHttpRequest();
    request.open('POST', '/change-user-info');
    request.setRequestHeader('X-CSRFToken', csrf_token);
    request.onload = function() {
        if (request.status == 200 || request.status == 400) {
            notify(request.responseText);
            document.querySelector('form#change-user-info input[type="submit"]').disabled = false;
        }
    }

    request.send(formData);
});
