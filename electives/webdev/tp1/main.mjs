"use strict";

import { fibo_it, fibonaRec, fiboArr, fiboMap } from "./exercise1.mjs";

import { wordCount, WordList } from "./exercise2.mjs";

import { Stud, FrStd } from "./exercise3.mjs";

import { Prmtn } from "./exercise4.mjs";

for (let n = 0; n < 10; n++)
    console.log(fibo_it(n));
console.log(fibo_it(100));
console.log()

for (let n = 0; n < 10; n++)
    console.log(fibonaRec(n));
console.log(fibonaRec(40));
console.log()

console.log(fiboArr([4, 5, 6, 7, 8, 100]));
console.log(fiboMap([4, 5, 6, 7, 8, 100]));

console.log();
console.log();

console.log(wordCount("fish bowl fish bowl fish"));
console.log(wordCount("É uma boa escola. Télecom Paris"));
console.log(wordCount("Lorem ipsum odor amet, consectetuer adipiscing elit. Feugiat diam interdum nullam venenatis litora commodo turpis. Volutpat eros hac malesuada posuere congue aptent maximus. Rutrum vivamus ligula magnis bibendum, nulla turpis quam tristique. Nec purus suscipit; dui potenti elementum class consequat. Rutrum commodo massa litora rutrum eget nec molestie lacus."));

const wl = new WordList("Lorem ipsum odor amet, consectetuer adipiscing elit. Feugiat diam interdum nullam venenatis litora commodo turpis. Volutpat eros hac malesuada posuere congue aptent maximus. Rutrum vivamus ligula magnis bibendum, nulla turpis quam tristique. Nec purus suscipit; dui potenti elementum class consequat. Rutrum commodo massa litora rutrum eget nec molestie lacus.")
console.log(wl.getWords())
console.log(wl.getCount("Rutrum"))
console.log(wl.minCountWord())
console.log(wl.maxCountWord())
console.log(wl.applyWordFunc(word => word.length))

console.log();
console.log();

const stud = new Stud("Vicentin", "Felipe", 1);
console.log(stud.toString());

const frstud = new FrStd("Olm", "Mariana", 23, "Brazilian");
console.log(frstud.toString());

console.log();
console.log();

const prmtn = new Prmtn();
prmtn.addStudent(stud);
prmtn.addStudent(frstud);

prmtn.print();

prmtn.saveF("teste.json");
prmtn.readFrom("teste.json");
