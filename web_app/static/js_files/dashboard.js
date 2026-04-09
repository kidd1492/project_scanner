
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
}

