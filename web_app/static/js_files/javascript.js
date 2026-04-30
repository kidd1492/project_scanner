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
            if (!list) return; // only on landing page

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
// Load project details on dashboard
// -----------------------------
function loadDashboard(projectName) {
    if (!projectName) return;

    fetch(`/api/project/${projectName}`)
        .then(r => r.json())
        .then(data => {
            if (data.error) {
                document.getElementById("dashboard-content").innerText = data.error;
                return;
            }

            document.getElementById("project-title").innerText = data.project_name;
            document.getElementById("file-count").innerText = data.total_files;
        })
        .catch(err => {
            console.error("Dashboard load error:", err);
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
