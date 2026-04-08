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

