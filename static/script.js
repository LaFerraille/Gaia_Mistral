if (document.querySelector(".main")) {
    document.querySelector(".main").onclick = function (){
        var submenu = document.querySelector(".spacer");
        submenu.classList.toggle("show");
    }
}


function sendChat() {
    var user_input = document.getElementById("user_input").value;
    var chat_messages = document.getElementById("chat_messages");
    var user_message = document.createElement("li");
    user_message.appendChild(document.createTextNode(user_input));
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
            mistral_message.appendChild(document.createTextNode(data));
            chat_messages.appendChild(mistral_message);
        });
}