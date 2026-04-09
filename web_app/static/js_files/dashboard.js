
// Tab switching
function showTab(type) {
    document.querySelectorAll('.analysis-window').forEach(div => {
        div.style.display = 'none';
    });

    document.getElementById(type).style.display = 'block';
    loadAnalysis(type);
}


// Load analysis JSON (html, js, api, classes, functions)
function loadAnalysis(type) {
    fetch(`/analysis/${PROJECT_NAME}/${type}`)
        .then(r => r.json())
        .then(data => {
            const box = document.getElementById(type);
            box.innerHTML = `
                <h3>${data.length} ${type.toUpperCase()}</h3><br/>
                <pre>${JSON.stringify(data, null, 4)}</pre>
            `;
        });
}

function loadFileList(type) {
    fetch(`/files/${PROJECT_NAME}/${type}`)
        .then(r => r.json())
        .then(data => {
            const box = document.getElementById("file-list-box");

            box.style.display = "block";
            box.innerHTML = `
                <h3>${data.files.length} ${type.toUpperCase()} FILES</h3>
                <ul>
                    ${data.files
                        .map(f => `<li class="file-item" onclick="loadFile('${f}')">${f}</li>`)
                        .join("")}
                </ul>
            `;

        });
}

function loadFile(filename) {
    // Load file content
    fetch(`/file/${encodeURIComponent(filename)}`)
        .then(r => r.json())
        .then(data => {
            const box = document.getElementById("file-display-box");
            box.style.display = "block";
            box.innerHTML = `
                <h3>${filename}</h3>
                <pre>${data.content}</pre>
            `;
        });

    // Load file analysis
    fetch(`/fileinfo/${PROJECT_NAME}/${encodeURIComponent(filename)}`)
        .then(r => r.json())
        .then(info => {
            const box = document.getElementById("file-analysis-box");
            box.style.display = "block";

            if (info.error) {
                box.innerHTML = `<p>No analysis available.</p>`;
                return;
            }

            box.innerHTML = buildFileAnalysisHTML(info);
        });
}


function buildFileAnalysisHTML(info) {
    return `
        <h3>Analysis Summary</h3>
        <p><b>Type:</b> ${info.type}</p>

        <ul>
            <li><b>HTML Events:</b> ${info.html_events.length}</li>
            <li><b>JS Functions:</b> ${info.js_functions.length}</li>
            <li><b>API Calls:</b> ${info.api_calls.length}</li>
            <li><b>Routes:</b> ${info.routes.length}</li>
            <li><b>Classes:</b> ${info.classes.length}</li>
            <li><b>Functions:</b> ${info.functions.length}</li>
        </ul>

        ${renderSection("HTML Events", info.html_events, e => `${e.event} → ${e.function}`)}
        ${renderSection("JS Functions", info.js_functions, f => `${f.function}()`)}
        ${renderSection("API Calls", info.api_calls, a => a)}
        ${renderSection("Routes", info.routes, r => `${r.route} → ${r.function}()`)}
        ${renderSection("Classes", info.classes, c => `${c.class} (${c.methods.length} methods)`)}
        ${renderSection("Functions", info.functions, f => `${f.function}(${f.args.join(", ")})`)}
    `;
}

function renderSection(title, items, formatter) {
    if (!items || items.length === 0) return "";
    return `
        <h4>${title}</h4>
        <ul>
            ${items.map(i => `<li>${formatter(i)}</li>`).join("")}
        </ul>
    `;
}
