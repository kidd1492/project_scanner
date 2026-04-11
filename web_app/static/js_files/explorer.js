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
// Load file details (symbols inside file)
// ---------------------------------------------------------
function loadFileDetails(path) {
    fetch(`/explorer/${PROJECT_NAME}/file/${encodeURIComponent(path)}`)
        .then(r => r.json())
        .then(file => {
            const box = document.getElementById("file-details");

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
                ${renderSymbolList("Classes", file.classes)}
                ${renderSymbolList("JS Functions", file.js_functions)}
                ${renderSymbolList("HTML Events", file.html_events)}
            `;
        });
}


// ---------------------------------------------------------
// Render symbol list with clickable items
// ---------------------------------------------------------
function renderSymbolList(title, items) {
    if (!items || items.length === 0) return "";

    return `
        <h4>${title}</h4>
        <ul>
            ${items
                .map(i => `<li onclick="loadSymbolDetails('${i.symbol_id}')">${i.name}</li>`)
                .join("")}
        </ul>
    `;
}


// ---------------------------------------------------------
// Load symbol details (args, calls, returns, relationships)
// ---------------------------------------------------------
function loadSymbolDetails(symbol_id) {
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
        });
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
