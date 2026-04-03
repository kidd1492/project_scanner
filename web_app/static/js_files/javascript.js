// ===============================
// index.js — for index.html only
// ===============================

// Load existing projects on page load
window.onload = () => {
    fetch("/project/load")
        .then(r => r.json())
        .then(data => {
            const list = document.getElementById("project-list");

            if (!data.results || data.results.length === 0) {
                list.innerHTML = "<p>No saved projects found.</p>";
                return;
            }

            list.innerHTML = data.results
                .map(name => `<li><a href="/dashboard/${name}">${name}</a></li>`)
                .join("");
        });
};


// Scan a new project
function scanProject() {
    const path = document.getElementById("project-path").value;

    if (!path) {
        alert("Please enter a project path.");
        return;
    }

    fetch(`/project/${encodeURIComponent(path)}`)
        .then(r => r.json())
        .then(data => {
            if (data.results) {
                alert("Project folder exists.");
                return; // <-- STOP HERE
            }

            alert("Project scanned successfully.");
            window.location.href = `/dashboard/${data.project_name}`;
        });
}

