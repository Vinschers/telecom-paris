"use strict";

import fs from "fs";
import { Stud, FrStd } from "./exercise3.mjs";

export class Prmtn {
    constructor() {
        this.students = [];
    }

    addStudent(student) {
        this.students.push(student);
    }

    size() {
        return this.students.length;
    }

    get(i) {
        if (i >= this.size()) return null;
        return this.students[i];
    }

    print() {
        let string = "";

        for (let student of this.students) {
            string += student.toString() + "\n";
        }

        console.log(string);
        return string;
    }

    write() {
        return JSON.stringify(this.students);
    }

    read(str) {
        const arr = JSON.parse(str);
        this.students = [];

        for (let obj of arr) {
            if (obj["nationality"])
                this.students.push(
                    new FrStd(
                        obj["lastName"],
                        obj["firstName"],
                        obj["id"],
                        obj["nationality"],
                    ),
                );
            else
                this.students.push(
                    new Stud(obj["lastName"], obj["firstName"], obj["id"]),
                );
        }
    }

    saveF(fileName) {
        const json = this.write();
        fs.writeFileSync(fileName, json);
    }

    readFrom(fileName) {
        const json = fs.readFileSync(fileName);
        this.read(json);
    }
}
