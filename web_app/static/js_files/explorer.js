document.addEventListener("DOMContentLoaded", () => {
    loadFileList();
});

// ---------------------------------------------------------
// Load all files from IR
// ---------------------------------------------------------
function loadFileList() {
    fetch(`/explorer/${PROJECT_NAME}/files`)
        .then(r => r.json())
        .then(files => {
            const list = document.getElementById("file-list");
            list.innerHTML = files
                .map(f => `<li onclick="loadFileDetails('${f.path}')">${f.path}</li>`)
                .join("");
        });
}

// ---------------------------------------------------------
// Load file details + source code
// ---------------------------------------------------------
function loadFileDetails(path) {
    fetch(`/explorer/${PROJECT_NAME}/file/${encodeURIComponent(path)}`)
        .then(r => r.json())
        .then(file => {
            const box = document.getElementById("file-details");
            console.log("FILE DETAILS:", file);

            box.innerHTML = `
                <h4>${file.path}</h4>
                <ul>
                    <li><b>Routes:</b> ${file.routes.length}</li>
                    <li><b>Functions:</b> ${file.functions.length}</li>
                    <li><b>Classes:</b> ${file.classes.length}</li>
                    <li><b>Imports:</b> ${file.imports.length}</li>
                    <li><b>JS Functions:</b> ${file.js_functions.length}</li>
                    <li><b>HTML Events:</b> ${file.html_events.length}</li>
                </ul>

                ${renderSymbolList("Routes", file.routes)}
                ${renderSymbolList("Functions", file.functions)}
                ${renderClassList(file.classes)}
                ${renderSymbolList("JS Functions", file.js_functions)}
                ${renderSymbolList("HTML Events", file.html_events)}
            `;

            loadSourceCode(path);
        });
}

// ---------------------------------------------------------
// Render symbol list (flat items with symbol_id)
// ---------------------------------------------------------
function renderSymbolList(title, items) {
    if (!items || items.length === 0) return "";

    return `
        <h4>${title}</h4>
        <ul>
            ${items
                .map(i => `<li onclick="loadSymbolDetails('${i.symbol_id}', ${i.line})">${i.name}</li>`)
                .join("")}
        </ul>
    `;
}

// ---------------------------------------------------------
// Render classes + nested methods
// ---------------------------------------------------------
function renderClassList(classes) {
    if (!classes || classes.length === 0) return "";

    let html = `<h4>Classes</h4><ul>`;

    classes.forEach(cls => {
        html += `<li><b>${cls.name}</b>`;

        // Render methods under each class
        if (cls.methods && cls.methods.length > 0) {
            html += `<ul>`;
            cls.methods.forEach(m => {
                html += `
                    <li onclick="loadSymbolDetails('${m.symbol_id}', ${m.line})">
                        ${m.name}
                    </li>`;
            });
            html += `</ul>`;
        }

        html += `</li>`;
    });

    html += `</ul>`;
    return html;
}

// ---------------------------------------------------------
// Load symbol details + scroll to line + highlight
// ---------------------------------------------------------
function loadSymbolDetails(symbol_id, line) {
    if (!symbol_id) {
        console.warn("No symbol_id provided — likely a class (classes have no symbol details).");
        return;
    }

    fetch(`/explorer/${PROJECT_NAME}/symbol/${encodeURIComponent(symbol_id)}`)
        .then(r => r.json())
        .then(sym => {
            const box = document.getElementById("symbol-details");

            box.innerHTML = `
                <h4>${sym.name}</h4>
                <p><b>Type:</b> ${sym.type}</p>
                <p><b>File:</b> ${sym.file}</p>
                <p><b>Line:</b> ${sym.line}</p>

                ${renderList("Args", sym.args)}
                ${renderList("Calls", sym.calls)}
                ${renderList("Returns", sym.returns ? [sym.returns] : [])}
            `;

            scrollToLine(sym.line);
        });
}

// ---------------------------------------------------------
// Load source code + highlight
// ---------------------------------------------------------
function loadSourceCode(path) {
    fetch(`/explorer/${PROJECT_NAME}/source/${encodeURIComponent(path)}`)
        .then(r => r.json())
        .then(data => {
            const codeBlock = document.querySelector("#code-viewer code");

            const safe = data.source
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;");

            codeBlock.innerHTML = safe;

            Prism.highlightAll();
        });
}

// ---------------------------------------------------------
// Scroll to a specific line in the code viewer
// ---------------------------------------------------------
function scrollToLine(line) {
    const viewer = document.getElementById("code-viewer");
    const codeLines = viewer.innerText.split("\n");

    if (line < 1 || line > codeLines.length) return;

    const approxHeight = 18; // px per line
    viewer.scrollTop = (line - 1) * approxHeight;

    highlightLine(line);
}

// ---------------------------------------------------------
// Highlight a specific line
// ---------------------------------------------------------
function highlightLine(line) {
    const viewer = document.getElementById("code-viewer");

    viewer.classList.remove("highlight-line");
    void viewer.offsetWidth;

    viewer.style.setProperty("--highlight-line", line);
    viewer.classList.add("highlight-line");
}

// ---------------------------------------------------------
// Helper: render list sections
// ---------------------------------------------------------
function renderList(title, items) {
    if (!items || items.length === 0) return "";
    return `
        <h4>${title}</h4>
        <ul>${items.map(i => `<li>${i}</li>`).join("")}</ul>
    `;
}


function renderClassList(classes) {
    if (!classes || classes.length === 0) return "";

    return `
        <h4>Classes</h4>
        <ul>
            ${classes.map(cls => `
                <li>
                    <span onclick="loadSymbolDetails('${cls.symbol_id}', ${cls.line})">
                        ${cls.name}
                    </span>

                    ${cls.methods && cls.methods.length > 0 ? `
                        <ul class="method-list">
                            ${cls.methods.map(m => `
                                <li onclick="loadSymbolDetails('${m.symbol_id}', ${m.line})">
                                    ${m.name}
                                </li>
                            `).join("")}
                        </ul>
                    ` : ""}
                </li>
            `).join("")}
        </ul>
    `;
}
