"use strict";

import * as http from "http";
import * as fs from "fs";
import { URL } from "url";

// Utility: safely read and parse storage.json
function readStorage() {
    try {
        let raw = fs.readFileSync("./storage.json", "utf8");
        return JSON.parse(raw);
    } catch (err) {
        console.error("Error reading storage.json:", err);
        // Return a default array if error
        return [{ title: "empty", color: "red", value: 1 }];
    }
}

// Utility: write out the given array to storage.json
function writeStorage(arr) {
    try {
        fs.writeFileSync(
            "./storage.json",
            JSON.stringify(arr, null, 2),
            "utf8",
        );
    } catch (err) {
        console.error("Error writing storage.json:", err);
    }
}

// Create the server
const server = http.createServer((req, res) => {
    try {
        let parsedUrl = new URL(req.url, `http://${req.headers.host}`);
        let pathname = parsedUrl.pathname;

        // 1) Answer something on "/" – just to confirm the server works
        if (pathname === "/") {
            res.writeHead(200, { "Content-Type": "text/plain" });
            res.end("Hello from server1.mjs, version 1.0");
            return;
        }

        // 2) Serve static files from current folder when URL starts with "/Root/"
        if (pathname.startsWith("/Root/")) {
            let localPath = "." + pathname.replace("/Root", "");
            // e.g. /Root/client/test2.html => ./client/test2.html
            try {
                let data = fs.readFileSync(localPath);
                // Very rough content-type guess
                let ctype = "text/plain";
                if (localPath.endsWith(".html")) ctype = "text/html";
                if (localPath.endsWith(".js")) ctype = "application/javascript";
                if (localPath.endsWith(".css")) ctype = "text/css";
                if (localPath.endsWith(".svg")) ctype = "image/svg+xml";
                if (localPath.endsWith(".json")) ctype = "application/json";

                res.writeHead(200, { "Content-Type": ctype });
                res.end(data);
            } catch (err) {
                res.writeHead(404, { "Content-Type": "text/plain" });
                res.end("Not found " + localPath);
            }
            return;
        }

        // 3) Exit the server on "/exit"
        if (pathname === "/exit") {
            res.writeHead(200, { "Content-Type": "text/plain" });
            res.end("Server exiting...");
            process.exit(0);
        }

        // ----------------------------------------------------
        // Additional routes for the assignment:
        // /Items -> returns the JSON
        // /add   -> add?title=...&value=...&color=...
        // /remove-> remove?index=...
        // /clear -> reset JSON to [ { "title":"empty","color":"red","value":1 } ]
        // /restore -> restore JSON to 3 slices
        // /PieCh -> return an SVG of the current slices
        // ----------------------------------------------------

        if (pathname === "/Items") {
            try {
                let arr = readStorage();
                res.writeHead(200, { "Content-Type": "application/json" });
                res.end(JSON.stringify(arr));
            } catch (err) {
                res.writeHead(500, { "Content-Type": "text/plain" });
                res.end("Error reading items: " + err);
            }
            return;
        }

        if (pathname === "/add") {
            try {
                let arr = readStorage();
                let title = parsedUrl.searchParams.get("title") || "unknown";
                let color = parsedUrl.searchParams.get("color") || "gray";
                let value =
                    parseFloat(parsedUrl.searchParams.get("value")) || 0;

                // Ensure strictly positive
                if (value <= 0) {
                    throw new Error("Value must be a positive number");
                }

                arr.push({ title, color, value });
                writeStorage(arr);

                res.writeHead(200, { "Content-Type": "application/json" });
                res.end(JSON.stringify({ msg: "Added element successfully!" }));
            } catch (err) {
                res.writeHead(500, { "Content-Type": "text/plain" });
                res.end("Error adding element: " + err);
            }
            return;
        }

        if (pathname === "/remove") {
            try {
                let arr = readStorage();
                let idx = parseInt(parsedUrl.searchParams.get("index"), 10);
                if (idx < 0 || idx >= arr.length) {
                    throw new Error("Invalid index");
                }
                arr.splice(idx, 1);
                writeStorage(arr);
                res.writeHead(200, { "Content-Type": "text/plain" });
                res.end("Removed element successfully!");
            } catch (err) {
                res.writeHead(500, { "Content-Type": "text/plain" });
                res.end("Error removing element: " + err);
            }
            return;
        }

        if (pathname === "/clear") {
            try {
                let arr = [{ title: "empty", color: "red", value: 1 }];
                writeStorage(arr);
                res.writeHead(200, { "Content-Type": "text/plain" });
                res.end("Cleared to single 'empty' slice.");
            } catch (err) {
                res.writeHead(500, { "Content-Type": "text/plain" });
                res.end("Error clearing: " + err);
            }
            return;
        }

        if (pathname === "/restore") {
            try {
                let arr = [
                    { title: "slice1", color: "red", value: 10 },
                    { title: "slice2", color: "blue", value: 20 },
                    { title: "slice3", color: "green", value: 5 },
                ];
                writeStorage(arr);
                res.writeHead(200, { "Content-Type": "text/plain" });
                res.end("Restored default slices.");
            } catch (err) {
                res.writeHead(500, { "Content-Type": "text/plain" });
                res.end("Error restoring: " + err);
            }
            return;
        }

        if (pathname === "/PieCh") {
            try {
                let arr = readStorage();
                if (!arr || arr.length === 0) {
                    throw new Error("No data to draw the pie chart.");
                }

                // Prepare to draw
                let total = arr.reduce((sum, el) => sum + el.value, 0);
                let cx = 200; // center x
                let cy = 200; // center y
                let r = 180; // radius
                let angleStart = 0; // in radians

                // Start building the SVG
                let svgParts = [];
                svgParts.push(
                    `<svg id="svg1" width="400" height="400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">`,
                );

                arr.forEach((slice, i) => {
                    let fraction = slice.value / total;
                    let angleEnd = angleStart + fraction * 2 * Math.PI;

                    // Coordinates for arc
                    let x1 = cx + r * Math.cos(angleStart);
                    let y1 = cy + r * Math.sin(angleStart);
                    let x2 = cx + r * Math.cos(angleEnd);
                    let y2 = cy + r * Math.sin(angleEnd);

                    // largeArcFlag is 1 if the angle is >= 180 degrees
                    let largeArcFlag = angleEnd - angleStart > Math.PI ? 1 : 0;

                    // Build the path command:
                    // Move to center, line to (x1, y1),
                    // arc to (x2, y2) with radius r
                    // close path
                    let d = [
                        `M ${cx},${cy}`,
                        `L ${x1},${y1}`,
                        `A ${r},${r} 0 ${largeArcFlag} 1 ${x2},${y2}`,
                        `Z`,
                    ].join(" ");

                    // Draw the wedge
                    svgParts.push(
                        `<path d="${d}" fill="${slice.color}" stroke="#000" stroke-width="1"/>`,
                    );

                    // Compute midpoint angle for text
                    let midAngle = angleStart + (angleEnd - angleStart) / 2;
                    let textX = cx + r * 0.6 * Math.cos(midAngle);
                    let textY = cy + r * 0.6 * Math.sin(midAngle);

                    let pct = ((slice.value / total) * 100).toFixed(1);

                    // Decide on text color so that it stands out
                    // You could do a more elaborate color contrast check
                    // Here let's just do white if slice.color is "dark", else black:
                    // (Very naive approach if color is not hex but a color name.)
                    let textColor = "#000000";
                    // Optionally look for dark color keywords or parse hex if you want more robust logic:
                    // e.g. if (slice.color === 'black' || slice.color === '#000000') textColor = '#ffffff';

                    svgParts.push(`<text x="${textX}" y="${textY}" fill="${textColor}" text-anchor="middle" alignment-baseline="middle" font-size="14">
             ${slice.title} (${pct}%)
          </text>`);

                    angleStart = angleEnd;
                });

                svgParts.push("</svg>");

                let svgStr = svgParts.join("\n");
                res.writeHead(200, { "Content-Type": "image/svg+xml" });
                res.end(svgStr);
            } catch (err) {
                res.writeHead(500, { "Content-Type": "text/plain" });
                res.end("Error building pie chart: " + err);
            }
            return;
        }

        // If no route matched:
        res.writeHead(404, { "Content-Type": "text/plain" });
        res.end("Not found");
    } catch (err) {
        // catch-all
        res.writeHead(500, { "Content-Type": "text/plain" });
        res.end("Server error: " + err);
    }
});

const PORT = parseInt(process.argv[2]) || 8000;
// Start listening
server.listen(PORT, () => {
    console.log("Server listening on http://localhost:" + PORT + "/");
});
