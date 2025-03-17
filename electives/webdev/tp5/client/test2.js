// A helper to simplify fetch calls that returns text
async function getText(url) {
    let resp = await fetch(url);
    if (!resp.ok) {
        throw new Error("HTTP error " + resp.status);
    }
    return await resp.text();
}

// A helper to simplify fetch calls that returns JSON
async function getJSON(url) {
    let resp = await fetch(url);
    if (!resp.ok) {
        throw new Error("HTTP error " + resp.status);
    }
    return await resp.json();
}

// Show the "add form" and hide the others
function showAddForm() {
    document.getElementById("addForm").style.display = "block";
    document.getElementById("removeForm").style.display = "none";
    document.getElementById("MAINSHOW").innerHTML = "";
}

// Show the "remove form" and hide the others
function showRemoveForm() {
    document.getElementById("removeForm").style.display = "block";
    document.getElementById("addForm").style.display = "none";
    document.getElementById("MAINSHOW").innerHTML = "";
}

// Clear forms and show the main area
function hideForms() {
    document.getElementById("addForm").style.display = "none";
    document.getElementById("removeForm").style.display = "none";
}

// Button handlers
document.getElementById("SHOW_B").addEventListener("click", async () => {
    hideForms();
    try {
        let data = await getJSON("../../Items");
        let out = JSON.stringify(data, null, 2);
        document.getElementById("MAINSHOW").textContent = out;
    } catch (err) {
        document.getElementById("MAINSHOW").textContent = "Error: " + err;
    }
});

document.getElementById("ADD_B").addEventListener("click", () => {
    showAddForm();
});

document.getElementById("REMOVE").addEventListener("click", () => {
    showRemoveForm();
});

document.getElementById("CLEAR").addEventListener("click", async () => {
    hideForms();
    try {
        let txt = await getText("../../clear");
        document.getElementById("MAINSHOW").textContent = txt;
    } catch (err) {
        document.getElementById("MAINSHOW").textContent = "Error: " + err;
    }
});

document.getElementById("RESTORE").addEventListener("click", async () => {
    hideForms();
    try {
        let txt = await getText("../../restore");
        document.getElementById("MAINSHOW").textContent = txt;
    } catch (err) {
        document.getElementById("MAINSHOW").textContent = "Error: " + err;
    }
});

// The "Add to JSON" button inside the addForm
document.getElementById("DOADD").addEventListener("click", async () => {
    let title = document.getElementById("titleTF").value;
    let color = document.getElementById("colorTF").value;
    let value = document.getElementById("valueTF").value;
    try {
        let txt = await getText(
            `../../add?title=${encodeURIComponent(title)}&color=${encodeURIComponent(color)}&value=${encodeURIComponent(value)}`,
        );
        document.getElementById("MAINSHOW").textContent = txt;
    } catch (err) {
        document.getElementById("MAINSHOW").textContent = "Error: " + err;
    }
});

// The "Remove from JSON" button inside the removeForm
document.getElementById("SENDREM").addEventListener("click", async () => {
    let idx = document.getElementById("indexTF").value;
    try {
        let txt = await getText(
            `../../remove?index=${encodeURIComponent(idx)}`,
        );
        document.getElementById("MAINSHOW").textContent = txt;
    } catch (err) {
        document.getElementById("MAINSHOW").textContent = "Error: " + err;
    }
});

// The "show piechart" button
document.getElementById("PIE").addEventListener("click", async () => {
    hideForms();
    try {
        // We fetch the piechart SVG from ../../PieCh
        // Then display it as an <img> or embed the raw SVG
        let pieUrl = "../../PieCh";
        let svgResp = await getText(pieUrl);
        document.getElementById("MAINSHOW").innerHTML = svgResp;
    } catch (err) {
        document.getElementById("MAINSHOW").textContent = "Error: " + err;
    }
});

document.getElementById("LOCAL_PIE").addEventListener("click", async () => {
    hideForms();
    try {
        // 1) Fetch the JSON data
        let data = await getJSON("../../Items");
        if (!data || data.length === 0) {
            document.getElementById("MAINSHOW").textContent =
                "No slices to show!";
            return;
        }

        // 2) Compute the total
        let total = data.reduce((acc, slice) => acc + slice.value, 0);

        // 3) Basic pie parameters
        let cx = 200;
        let cy = 200;
        let r = 180;
        let angleStart = 0;

        // 4) Start building the SVG string
        let svgParts = [
            `<?xml version="1.0" encoding="UTF-8"?>`,
            `<svg width="400" height="400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">`,
        ];

        // 5) Create each wedge
        data.forEach((slice) => {
            let fraction = slice.value / total;
            let angleEnd = angleStart + fraction * 2 * Math.PI;

            let x1 = cx + r * Math.cos(angleStart);
            let y1 = cy + r * Math.sin(angleStart);
            let x2 = cx + r * Math.cos(angleEnd);
            let y2 = cy + r * Math.sin(angleEnd);
            let largeArcFlag = angleEnd - angleStart > Math.PI ? 1 : 0;

            let d = [
                `M ${cx},${cy}`,
                `L ${x1},${y1}`,
                `A ${r},${r} 0 ${largeArcFlag} 1 ${x2},${y2}`,
                `Z`,
            ].join(" ");

            svgParts.push(
                `<path d="${d}" fill="${slice.color}" stroke="#000" stroke-width="1"/>`,
            );

            // Midpoint angle for the label
            let midAngle = angleStart + (angleEnd - angleStart) / 2;
            let textX = cx + r * 0.6 * Math.cos(midAngle);
            let textY = cy + r * 0.6 * Math.sin(midAngle);
            let pct = ((slice.value / total) * 100).toFixed(1);

            svgParts.push(`
        <text x="${textX}" y="${textY}" fill="#000"
          text-anchor="middle" alignment-baseline="middle" font-size="14">
          ${slice.title} (${pct}%)
        </text>`);

            angleStart = angleEnd;
        });

        // 6) Close the SVG
        svgParts.push(`</svg>`);

        // 7) Insert the SVG into MAINSHOW
        document.getElementById("MAINSHOW").innerHTML = svgParts.join("\n");
    } catch (err) {
        document.getElementById("MAINSHOW").textContent = "Error: " + err;
    }
});
