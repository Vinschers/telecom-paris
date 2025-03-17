"use strict";

const send = () => {
    const xhttp = new XMLHttpRequest();
    const textedit = document.getElementById("textedit");

    xhttp.onload = () => {
        textedit.value = "";
        update();
    };
    const phrase = textedit.value;
    xhttp.open("GET", `chat.php?phrase=${phrase}`, true);
    xhttp.send();
};

const update = () => {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function () {
        if (this.status === 404) {
            // not found, add some error handling
            return;
        }
        const div = document.getElementById("texta");
        const lines = this.responseText.split("\n").slice(-11).reverse();

        div.innerHTML = "";

        lines.forEach((line) => {
            if (line == "") return;
            const p = document.createElement("p");
            p.innerHTML = line.substring(line.indexOf("-") + 1);
            div.append(p);
        });
    };
    xhttp.open("GET", "chatlog.txt", true);
    xhttp.send();
};

update();
setInterval(update, 1000);
