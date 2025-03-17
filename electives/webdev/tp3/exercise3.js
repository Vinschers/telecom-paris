"use strict";

const display = (url) => {
    const div = document.getElementById("container");
    div.innerHTML = "";

    const iframe = document.createElement("iframe");
    iframe.src = url;
    iframe.height = 600;
    iframe.width = iframe.height * (16 / 9);

    div.append(iframe);
};

const play = () => {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function () {
        const slides = JSON.parse(this.responseText)["slides"];

        slides.forEach(slide => {
            setTimeout(() => {display(slide.url);}, slide.time * 1000);
        });
    };
    xhttp.open("GET", "slides.json", true);
    xhttp.send();
};
