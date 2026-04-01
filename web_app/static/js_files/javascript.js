// -------------------------
// Load existing project on page load
// -------------------------
window.onload = () => {
    fetch("/project/load")
        .then(r => r.json())
        .then(data => {
            if (data.exists === false) {
                document.getElementById("analysis-box").innerHTML =
                    "<p>No project loaded. Enter a path and scan.</p>";
                return;
            }
            renderProjectSummary(data);
        });
};


// -------------------------
// Render Project Summary
// -------------------------
function renderProjectSummary(project) {
    const box = document.getElementById("summary-box");

    box.innerHTML = `
        <h1>${project.project_name}</h1>
        <p><strong>Total Files:</strong> ${project.total_files}</p>

        <h4>File Types</h4>
        <ul>
            ${project.file_types.map(ft => `
                <li>${ft.type}: ${ft.count}</li>
            `).join("")}
        </ul>
    `;
}


// -------------------------
// Load analysis JSON (html, js, api, classes, functions)
// -------------------------
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



function scanProject() {
    const path = document.getElementById("project-path").value;

    if (!path) {
        alert("Please enter a project path.");
        return;
    }

    fetch(`/project/${encodeURIComponent(path)}`)
        .then(r => r.json())
        .then(data => {
            if(data.results)
                alert("Project Folder Exist")
            renderProjectSummary(data);
            alert("Project scanned successfully.");
        });
}


// -------------------------
// Rescan project
// -------------------------
function rescanProject() {
    const path = prompt("Enter project path to rescan:");
    if (!path) return;

    fetch(`/project/${encodeURIComponent(path)}`)
        .then(r => r.json())
        .then(() => window.location.reload());
}


function showTab(type) {
    document.querySelectorAll('.analysis-window').forEach(div => {
        div.style.display = 'none';
    });

    document.getElementById(type).style.display = 'block';

    // Load data only when tab is opened
    loadAnalysis(type);
}

