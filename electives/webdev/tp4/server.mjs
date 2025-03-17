"use strict";

import { createServer } from "http";
import fs from "fs";
import path from "path";
import { parse } from "querystring";

const loadFile = (req, res) => {
    const filePath = path.join(process.cwd(), req.url.replace("/root", ""));

    if (!filePath.startsWith(process.cwd())) {
        res.writeHead(403, { "Content-Type": "text/plain" });
        res.end("403 Forbidden");
        return;
    }

    fs.stat(filePath, (err, stats) => {
        if (err || !stats.isFile()) {
            res.writeHead(404, { "Content-Type": "text/plain" });
            res.end("404 Not Found");
            return;
        }

        const ext = path.extname(filePath).toLowerCase();
        const mimeTypes = {
            ".html": "text/html",
            ".css": "text/css",
            ".js": "application/javascript",
            ".mjs": "application/javascript",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".json": "application/json",
            ".txt": "text/plain",
        };
        const mimeType = mimeTypes[ext];

        fs.readFile(filePath, (err, data) => {
            if (err) {
                res.writeHead(500, { "Content-Type": "text/plain" });
                res.end("500 Internal Server Error");
                return;
            }

            res.writeHead(200, { "Content-Type": mimeType });
            res.end(data);
        });
    });
};

const hello = (req, res) => {
    const query = req.url.split("?")[1];
    const params = parse(query);

    let user = params.user || "";
    user = decodeURIComponent(user);

    res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
    res.end(`<!doctype html><html><body>hello ${user}</body></html>`);
};

const users = [];

const ciao = (req, res) => {
    const query = req.url.split("?")[1];
    const params = parse(query);

    let user = params.name || "";
    user = user.replace(/</g, "_").replace(/>/g, "_");
    users.push(user);

    const previousUsers = users.slice(0, -1).join(", ") || "";
    const htmlResponse = `<!doctype html><html><body>ciao ${user}, the following users have already visited this page: ${previousUsers}</body></html>`;

    res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
    res.end(htmlResponse);
};

const clear = (req, res) => {
    users.length = 0;
    res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
    res.end("<!doctype html><html><body>users have been cleared</body></html>");
};

// process requests
function webserver(request, response) {
    response.setHeader("Content-Type", "text/html; charset=utf-8");

    if (request.url === "/exit") {
        response.end(
            "<!doctype html><html><body>The server will stop now.</body></html>",
        );
        process.exit(0);
    } else if (request.url.startsWith("/root")) {
        loadFile(request, response);
    } else if (request.url.startsWith("/hello")) {
        hello(request, response);
    } else if (request.url.startsWith("/ciao")) {
        ciao(request, response);
    } else if (request.url.startsWith("/clear")) {
        clear(request, response);
    } else {
        response.end("<!doctype html><html><body>Working!</body></html>");
    }
}

// instanciate server
const server = createServer((req, res) => {
    try {
        webserver(req, res);
    } catch (e) {
        console.error(e);
        res.end("500 Internal Server Error");
    }
});

const PORT = parseInt(process.argv[2]) || 8000;
// start the server
server.listen(PORT, (err) => {});
