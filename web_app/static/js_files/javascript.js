// Scan a new project
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


// Load dashboard data
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

            renderCharts(projectName);
        })
        .catch(err => console.error("Dashboard load error:", err));
}


// Render charts
function renderCharts(projectName) {
    const charts = {
        "chart-file-types": "file_types.png",
        "chart-symbols": "symbol_distribution.png",
        "chart-routes-js": "routes_vs_js.png",
        "chart-api-calls": "api_calls.png",
        "chart-html-events": "html_events.png"
    };

    Object.entries(charts).forEach(([id, file]) => {
        const img = document.getElementById(id);
        img.src = `/static/projects/${projectName}/${file}`;
    });
}


// Auto-run
window.addEventListener("DOMContentLoaded", () => {

    const dashboardRoot = document.getElementById("dashboard-root");
    if (dashboardRoot) {
        const projectName = dashboardRoot.dataset.project;
        loadDashboard(projectName);
    }
});
