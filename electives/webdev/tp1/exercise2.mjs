"use strict";

export function wordCount(string) {
    const hist = {};

    for (let word of string.split(" ")) {
        word = word.replace(/[^\p{L}\p{N}]/gu, ""); // Remove special characters, such as points, commas, etc.
        hist[word] = (hist[word] || 0) + 1; // If word appears for the first time, it is 0 + 1 = 1 in the histogram.
    }

    return hist;
}

export class WordList {
    constructor(string) {
        this.string = string;
        this.hist = wordCount(string);
    }

    getWords() {
        if (!this.words) this.words = Object.keys(this.hist).sort();
        return this.words;
    }

    maxCountWord() {
        let max = 0;
        let wordMax = "";

        for (let word of this.getWords()) {
            if (this.hist[word] > max) {
                // Usage of > guarantees that result will be first in lexicographic order.
                max = this.hist[word];
                wordMax = word;
            }
        }

        return wordMax;
    }

    minCountWord() {
        let min = this.hist[this.getWords()[0]]; // Use first word to avoid edge cases in the string.
        let wordMin = this.getWords()[0];

        for (let word of this.getWords()) {
            if (this.hist[word] < min) {
                // Usage of < guarantees that result will be first in lexicographic order.
                min = this.hist[word];
                wordMin = word;
            }
        }

        return wordMin;
    }

    getCount(word) {
        return this.hist[word] || 0;
    }

    applyWordFunc(f) {
        return this.getWords().map((word) => f(word));
    }
}
