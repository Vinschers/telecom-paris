"use strict";

const loadDoc = () => {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function () {
        document.getElementById("texta").innerHTML = this.responseText;
    };
    xhttp.open("GET", "text.txt", true);
    xhttp.send();
};

const loadDoc2 = () => {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function () {
        const div = document.getElementById("texta2");
        const lines = this.responseText.split("\n");
        const colors = ["red", "green", "blue", "magenta", "black"];
        let i = 0;

        div.innerHTML = "";

        lines.forEach((line) => {
            if (line == "") return;
            const p = document.createElement("p");
            p.innerHTML = line;
            p.style.color = colors[i++];
            div.appendChild(p);
        });
    };
    xhttp.open("GET", "text.txt", true);
    xhttp.send();
};
