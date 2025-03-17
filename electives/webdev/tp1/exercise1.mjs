"use strict";

// non recursive
export function fibo_it(n) {
    if (n <= 1) return n;

    let fib0 = 0; // n - 2
    let fib1 = 1; // n - 1

    for (let i = 2; i <= n; i++) {
        const fib = fib0 + fib1;

        fib0 = fib1;
        fib1 = fib;
    }

    return fib1;
}

// recursive version
export function fibonaRec(n) {
    if (n <= 1) return n;

    return fibonaRec(n - 1) + fibonaRec(n - 2);
}

// process array, no map
export function fiboArr(t) {
    const maxT = Math.max(...t);
    const memo = [0, 1];

    let fib0 = 0; // n - 2
    let fib1 = 1; // n - 1

    for (let i = 2; i <= maxT; i++) {
        const fib = fib0 + fib1;
        fib0 = fib1;
        fib1 = fib;

        memo.push(fib);
    }

    const result = [];
    for (let n of t) {
        result.push(memo[n]);
    }

    return result;
}

// use of map
export function fiboMap(t) {
    return t.map(n => fibo_it(n));
}
