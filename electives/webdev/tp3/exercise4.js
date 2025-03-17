"use strict";

const iframes = [];
let slides = [];
let idx = -1;
let playing = false;

const display = () => {
    const div = document.getElementById("container");
    div.innerHTML = "";
    div.append(iframes[idx]);
};

const load = () => {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function () {
        slides = JSON.parse(this.responseText)["slides"];

        slides.forEach((slide) => {
            const iframe = document.createElement("iframe");
            iframe.src = slide.url;
            iframe.height = 600;
            iframe.width = iframe.height * (16 / 9);

            iframes.push(iframe);
        });
    };
    xhttp.open("GET", "slides.json", true);
    xhttp.send();
};

load();

const play = () => {
    idx = 0;
    playing = true;
    update();
};

const next = () => {
    if (idx == slides.length - 1)
        idx = -1;
    idx++;
    display();
};

const previous = () => {
    if (idx == 0)
        idx = slides.length;
    idx--;
    display();
};

const update = () => {
    if (!playing || idx + 1 == slides.length) return;

    const delta = slides[idx + 1].time - slides[idx].time;
    setTimeout(() => {
        if (playing) {
            next();
            update();
        }
    }, delta * 1000);
};

const nextBtn = () => {
    playing = false;
    next();
};

const previousBtn = () => {
    playing = false;
    previous();
};

const pause_continue = () => {
    playing = !playing;
    update();
};
