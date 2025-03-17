"use strict";

// ---------------------------------------------------------------------
// Imports
// ---------------------------------------------------------------------
import express from "express";
import fs from "fs";
import morgan from "morgan";

// ---------------------------------------------------------------------
// Express application and middleware
// ---------------------------------------------------------------------
const app = express();

// Morgan for request logging
app.use(morgan("dev"));

// Middleware for JSON body parsing in POST/PUT
app.use(express.json());

// ---------------------------------------------------------------------
// Load the in-memory database
// ---------------------------------------------------------------------
let db = [];

/**
 * Loads the JSON database from the file db.json
 */
function loadDatabase() {
    try {
        const data = fs.readFileSync("db.json", "utf8");
        db = JSON.parse(data);
    } catch (err) {
        console.error("Error loading db.json:", err.message);
        // If loading or parsing fails, keep db as is (empty or stale)
    }
}

// Load the database at startup
loadDatabase();

// ---------------------------------------------------------------------
// Retrieve the port number from command line arguments
// ---------------------------------------------------------------------
const portArg = process.argv[2];
const PORT = portArg ? parseInt(portArg, 10) : 3000;

// ---------------------------------------------------------------------
// Question 0: Basic server with logging, /end, /restore
// ---------------------------------------------------------------------

/**
 * GET /
 * Simple route to say "Hi"
 */
app.get("/", (req, res) => {
    try {
        res.send("Hi");
    } catch (err) {
        console.error("Error in / route:", err.message);
        res.status(500).send(err.message);
    }
});

/**
 * GET /end
 * Shuts down the server (for automated testing)
 */
app.get("/end", (req, res) => {
    try {
        res.send("Server is ending...");
        setTimeout(() => process.exit(0), 100);
    } catch (err) {
        console.error("Error in /end route:", err.message);
        res.status(500).send(err.message);
    }
});

/**
 * GET /restore
 * Reloads db.json in memory
 */
app.get("/restore", (req, res) => {
    try {
        loadDatabase();
        res.setHeader("Content-Type", "text/plain");
        res.send("db.json reloaded");
    } catch (err) {
        console.error("Error in /restore route:", err.message);
        res.status(500).send(err.message);
    }
});

// ---------------------------------------------------------------------
// Question 1: GET /nbpapers => number of publications (plain text)
// ---------------------------------------------------------------------
app.get("/nbpapers", (req, res) => {
    try {
        const numberOfPapers = db.length;
        res.type("text/plain").send(numberOfPapers.toString());
    } catch (err) {
        console.error("Error in /nbpapers route:", err.message);
        res.status(500).send(err.message);
    }
});

// ---------------------------------------------------------------------
// Question 2: GET /authoredby/:name => count of pubs containing :name
// ---------------------------------------------------------------------
app.get("/authoredby/:name", (req, res) => {
    try {
        const searchStr = req.params.name.toLowerCase();
        let count = 0;

        db.forEach((pub) => {
            const hasMatchingAuthor = pub.authors.some((author) =>
                author.toLowerCase().includes(searchStr),
            );
            if (hasMatchingAuthor) {
                count += 1;
            }
        });

        res.type("text/plain").send(count.toString());
    } catch (err) {
        console.error("Error in /authoredby/:name route:", err.message);
        res.status(500).send(err.message);
    }
});

// ---------------------------------------------------------------------
// Question 3: GET /papersfrom/:name => list of pubs (JSON) matching :name
// ---------------------------------------------------------------------
app.get("/papersfrom/:name", (req, res) => {
    try {
        const searchStr = req.params.name.toLowerCase();
        const matchingPublications = db.filter((pub) =>
            pub.authors.some((author) =>
                author.toLowerCase().includes(searchStr),
            ),
        );
        res.type("application/json").send(JSON.stringify(matchingPublications));
    } catch (err) {
        console.error("Error in /papersfrom/:name route:", err.message);
        res.status(500).send(err.message);
    }
});

// ---------------------------------------------------------------------
// Question 4: GET /titles/:name => titles (JSON) whose authors match :name
// ---------------------------------------------------------------------
app.get("/titles/:name", (req, res) => {
    try {
        const searchStr = req.params.name.toLowerCase();

        // Find publications that match
        const matchingTitles = db
            .filter((pub) =>
                pub.authors.some((author) =>
                    author.toLowerCase().includes(searchStr),
                ),
            )
            .map((pub) => pub.title);

        // Return as JSON
        res.type("application/json").send(JSON.stringify(matchingTitles));
    } catch (err) {
        console.error("Error in /titles/:name route:", err.message);
        res.status(500).send(err.message);
    }
});

// ---------------------------------------------------------------------
// Question 5: GET /ref/:key => descriptor of the pub with this "key"
// ---------------------------------------------------------------------
app.get("/ref/:key", (req, res) => {
    try {
        const pubKey = req.params.key;
        // Find the publication whose key matches
        const publication = db.find((pub) => pub.key === pubKey);

        if (!publication) {
            // Not found
            res.status(404).send(`No publication found with key=${pubKey}`);
            return;
        }

        // Return the descriptor (the whole publication object) as JSON
        res.type("application/json").send(JSON.stringify(publication));
    } catch (err) {
        console.error("Error in /ref/:key route:", err.message);
        res.status(500).send(err.message);
    }
});

// ---------------------------------------------------------------------
// Question 6: DELETE /ref/:key => delete pub with this "key" in memory
// ---------------------------------------------------------------------
app.delete("/ref/:key", (req, res) => {
    try {
        const pubKey = req.params.key;
        const initialLength = db.length;
        // Filter out the publication with the matching key
        db = db.filter((pub) => pub.key !== pubKey);

        if (db.length === initialLength) {
            // Means nothing was removed => key not found
            res.status(404).send(`No publication found with key=${pubKey}`);
        } else {
            // Some publication was removed
            res.send(`Publication with key=${pubKey} removed`);
        }
    } catch (err) {
        console.error("Error in DELETE /ref/:key route:", err.message);
        res.status(500).send(err.message);
    }
});

// ---------------------------------------------------------------------
// Question 7: POST /ref => add a new publication with key = "imaginary"
// ---------------------------------------------------------------------
app.post("/ref", (req, res) => {
    try {
        // We force the key to be "imaginary"
        const newPublication = { ...req.body, key: "imaginary" };

        db.push(newPublication);

        res.status(201).send(`New publication added with key=imaginary`);
    } catch (err) {
        console.error("Error in POST /ref route:", err.message);
        res.status(500).send(err.message);
    }
});

// ---------------------------------------------------------------------
// Question 8: PUT /ref/:key => update partial fields of the publication
// ---------------------------------------------------------------------
app.put("/ref/:key", (req, res) => {
    try {
        const pubKey = req.params.key;
        const publicationIndex = db.findIndex((pub) => pub.key === pubKey);

        if (publicationIndex === -1) {
            // If not found
            return res
                .status(404)
                .send(`No publication found with key=${pubKey}`);
        }

        // We only update fields present in req.body. Others remain the same.
        const existingPublication = db[publicationIndex];
        const updatedPublication = {
            ...existingPublication,
            ...req.body, // overwrite only the fields in the request
        };

        db[publicationIndex] = updatedPublication;
        res.send(`Publication with key=${pubKey} updated`);
    } catch (err) {
        console.error("Error in PUT /ref/:key route:", err.message);
        res.status(500).send(err.message);
    }
});

// ---------------------------------------------------------------------
// Start the server
// ---------------------------------------------------------------------
app.listen(PORT, () => {
    console.log(`Server started on port ${PORT}`);
    console.log(`Visit http://localhost:${PORT} in your browser`);
});
