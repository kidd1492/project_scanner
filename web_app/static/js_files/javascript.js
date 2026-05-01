// -----------------------------
// Scan a new project
// -----------------------------
function scanProject() {
    const path = document.getElementById("project-path").value;

    if (!path) {
        alert("Please enter a project path.");
        return;
    }

    fetch("/api/scan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ path })
    })
    .then(r => r.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }

        alert("Project scanned successfully.");
        window.location.href = `/dashboard/${data.project_name}`;
    })
    .catch(err => {
        console.error("Scan error:", err);
        alert("An error occurred while scanning the project.");
    });
}


// -----------------------------
// Load list of scanned projects
// -----------------------------
function loadProjects() {
    fetch("/api/projects")
        .then(r => r.json())
        .then(data => {
            const list = document.getElementById("project-list");
            if (!list) return;

            list.innerHTML = "";

            if (data.projects.length === 0) {
                list.innerHTML = "<li>No projects found</li>";
                return;
            }

            data.projects.forEach(name => {
                const li = document.createElement("li");
                li.innerHTML = `<a href="/dashboard/${name}">${name}</a>`;
                list.appendChild(li);
            });
        })
        .catch(err => {
            console.error("Project list error:", err);
        });
}


// -----------------------------
// Load dashboard data
// -----------------------------
function loadDashboard(projectName) {
    if (!projectName) return;

    fetch(`/api/dashboard/${projectName}`)
        .then(r => r.json())
        .then(data => {
            if (data.error) {
                document.getElementById("dashboard-content").innerText = data.error;
                return;
            }
            const box = document.getElementById("overview-content");
            // Summary
            box.innerHTML = `
                <ul>
                    <li><b>Total Files:</b> ${data.total_files}</li>

                    <li><b>Python Files:</b> ${data.file_type_counts.py}</li>
                    <li><b>JS Files:</b> ${data.file_type_counts.js}</li>
                    <li><b>HTML Files:</b> ${data.file_type_counts.html}</li>
                    <li><b>CSS Files:</b> ${data.file_type_counts.css}</li>

                    <li><b>Functions:</b> ${data.symbol_counts.functions}</li>
                    <li><b>Classes:</b> ${data.symbol_counts.classes}</li>
                    <li><b>Methods:</b> ${data.symbol_counts.methods}</li>
                    <li><b>Imports:</b> ${data.symbol_counts.imports}</li>

                    <li><b>Routes:</b> ${data.routes}</li>
                    <li><b>JS Functions:</b> ${data.js_functions}</li>
                    <li><b>HTML Events:</b> ${data.html_events}</li>
                    <li><b>API Calls:</b> ${data.api_calls}</li>
                </ul>
            `;


            // Charts
            renderCharts(projectName);
        })
        .catch(err => {
            console.error("Dashboard load error:", err);
        });
}


// -----------------------------
// Render charts (PNG images)
// -----------------------------
function renderCharts(projectName) {
    const container = document.getElementById("chart-container");
    if (!container) return;

    const charts = [
        "file_types.png",
        "symbol_distribution.png",
        "routes_vs_js.png",
        "api_calls.png",
        "html_events.png"
    ];

    charts.forEach(name => {
        const img = document.createElement("img");
        img.src = `/static/projects/${projectName}/${name}`;
        img.classList.add("chart-image");
        container.appendChild(img);
    });
}


// -----------------------------
// Auto-run on page load
// -----------------------------
window.addEventListener("DOMContentLoaded", () => {
    loadProjects();
    

    const dashboardRoot = document.getElementById("dashboard-root");
    if (dashboardRoot) {
        const projectName = dashboardRoot.dataset.project;
        loadDashboard(projectName);
    }
});
