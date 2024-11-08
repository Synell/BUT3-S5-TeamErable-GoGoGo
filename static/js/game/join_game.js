htmx.config.useTemplateFragments = true;
document.querySelector("#search-input").addEventListener('keyup', function(event) {
    var formData = new FormData();
    formData.append('game_name', event.target.value);

    var csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    var request = new XMLHttpRequest();
    request.open('POST', '/search-game');
    request.setRequestHeader('X-CSRFToken', csrf_token);
    request.onload = function() {
        if (request.status == 200) {
            document.querySelector("#game-list").innerHTML = request.responseText;
            htmx.process(document.querySelector("#game-list"));
        }
    }
    request.send(formData);
});

document.querySelectorAll(".pass-to-next").forEach(function(element) {
    element.addEventListener('paste', function(event) {
        var pastedText = event.clipboardData.getData('text');
        var input = event.target;

        for (var i = 0; i < pastedText.length; i++) {
            while (input.value.length == 4) {
                var newinput = input.nextElementSibling.nextElementSibling;
                if (newinput.type == "text") {
                    input = newinput;
                    input.focus();
                }
                else break;
            }
            if (input.type != "text") break;
            if (input.value.length == 4) break;
            input.value += pastedText[i];
        }
        event.preventDefault();
    });

    element.addEventListener('keyup', function(event) {
        event.target.value = event.target.value.toUpperCase();
        event.target.value = event.target.value.replace(/[^A-Z0-9]/g, '');

        if (event.target.value.length == 4) {
            event.target.nextElementSibling.nextElementSibling.focus();
        }
    })
});

document.querySelector(".pass-to-next-last").addEventListener('keyup', function(event) {
    event.target.value = event.target.value.toUpperCase();
    event.target.value = event.target.value.replace(/[^A-Z0-9]/g, '');
});

document.querySelector("form#join-by-code").addEventListener('submit', function(event) {
    event.target.querySelector("input[type='submit']").disabled = true;
    event.preventDefault();
    var formData = new FormData(event.target);
    var csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    var request = new XMLHttpRequest();
    request.open('POST', '/game-code');
    formData.append(
        'code',
        event.target.querySelector("#search-code-input-0").value +
        event.target.querySelector("#search-code-input-1").value +
        event.target.querySelector("#search-code-input-2").value +
        event.target.querySelector("#search-code-input-3").value
    )
    request.setRequestHeader('X-CSRFToken', csrf_token);
    request.onload = function() {
        if (request.status == 400) {
            notify(request.responseText);
            event.target.querySelector("input[type='submit']").disabled = false;
        } else if (request.status == 200) {
            window.location.href = request.responseText;
        }
    }
    request.send(formData);
});
