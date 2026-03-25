
function loadExistingProject() {
    fetch("/project/load")
        .then(r => r.json())
        .then(data => {
            if (data.exists === false) {
                document.getElementById("summary-box").innerHTML =
                    "<p>No project loaded…</p>";
                return;
            }
            displayProjectSummary(data);
        });
}


// -------------------------
// Scan a new project
// -------------------------
function scanProject() {
    const term = document.getElementById("project-path").value;

    if (!term) {
        alert("Please enter a project path.");
        return;
    }

    fetch(`/project/${encodeURIComponent(term)}`)
        .then(r => r.json())
        .then(data => displayProjectSummary(data));
}


// -------------------------
// Display project summary
// -------------------------
function displayProjectSummary(data) {
    const box = document.getElementById("summary-box");

    box.innerHTML = `
        <h3>Project: ${data.project_name}</h3>
        <p><strong>Total Files:</strong> ${data.total_files}</p>

        <h4>File Types</h4>
        <ul>
            ${data.file_types.map(ft => `
                <li onclick="loadFileList('${ft.type}')">
                    ${ft.type}: ${ft.count}
                </li>
            `).join("")}
        </ul>
    `;
}


// -------------------------
// Load files for a file type
// -------------------------
function loadFileList(fileType) {
    fetch(`/project/files/${fileType}`)
        .then(r => r.json())
        .then(data => {
            const box = document.getElementById("file-box");

            if (data.exists === false) {
                box.innerHTML = "<p>No project loaded…</p>";
                return;
            }

            box.innerHTML = `
                <h3>Files of type: ${fileType}</h3>
                <ul>
                    ${data.files.map(f => `<li>${f}</li>`).join("")}
                </ul>
            `;
        });
}

