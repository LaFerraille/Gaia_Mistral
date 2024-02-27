
if (document.querySelector(".main")) {
    document.querySelector(".main").onclick = function () {
        var submenu = document.querySelector("#menu_spacer");
        submenu.classList.toggle("show");
    }
}

if (document.querySelector("#profile")) {
    document.querySelector("#profile").onclick = function () {
        var submenu = document.querySelector("#profile_spacer");
        submenu.classList.toggle("show");
    }
}

if (document.querySelector("#weather")) {
    document.querySelector("#weather").onclick = function () {
        var submenu = document.querySelector("#weather_spacer");
        submenu.classList.toggle("show");
    }
}

if (document.querySelector("#news")) {
    document.querySelector("#news").onclick = function () {
        var submenu = document.querySelector("#news_spacer");
        submenu.classList.toggle("show");
    }
}

// videos
if (document.querySelector("#videos")) {
    document.querySelector("#videos").onclick = function () {
        var submenu = document.querySelector("#videos_spacer");
        submenu.classList.toggle("show");
    }
}

function sendChat() {
    var user_input = document.getElementById("user_input").value;
    var chat_messages = document.getElementById("chat_messages");

    var user_message = document.createElement("li");
    user_message.className = "chat-message"; // add a class to style the li elements

    var user_image = document.createElement("img");
    user_image.src = "static/agriculteur.png"; // replace with the actual path to the image
    user_image.id = "user-image"; // add an id to style the image
    user_message.appendChild(user_image);

    var user_text = document.createElement("span"); // wrap the text in a span element
    user_text.appendChild(document.createTextNode(user_input));
    user_message.appendChild(user_text);

    chat_messages.appendChild(user_message);
    document.getElementById("user_input").value = "";

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            user_input: user_input
        }),
    })
        .then(response => response.text())
        .then(data => {
            var mistral_message = document.createElement("li");
            mistral_message.className = "chat-message"; // add a class to style the li elements

            var mistral_image = document.createElement("img");
            mistral_image.src = "https://next.ink/wp-content/uploads/2024/02/announcing-mistral.png";
            mistral_image.id = "mistral-image"; // add an id to style the image
            mistral_message.appendChild(mistral_image);

            var mistral_text = document.createElement("b"); // wrap the text in a b element
            mistral_text.appendChild(document.createTextNode(data));
            mistral_message.appendChild(mistral_text);

            chat_messages.appendChild(mistral_message);
        });
}

function sendReport() {
    fetch('/report', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then(response => response.text())
        .then(data => {
            var report = document.createElement("li");
            report.className = "submenu"; // add a class to style the li elements

            var report_text = document.createElement("b"); // wrap the text in a b element
            report_text.appendChild(document.createTextNode(data));
            report.appendChild(report_text);

            document.querySelector("#profile ul").appendChild(report);
        });
}

