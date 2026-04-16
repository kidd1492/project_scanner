document.addEventListener("DOMContentLoaded", () => {
    loadOverview();
    loadCharts();
});


// ---------------------------------------------------------
// Load IR-based counts for overview panel
// ---------------------------------------------------------
function loadOverview() {
    fetch(`/counts/${PROJECT_NAME}`)

        .then(async r => {
            const raw = await r.text();
            try {
                return JSON.parse(raw);
            } catch (e) {
                return null;
            }
        })
        .then(counts => {
            console.log("Parsed counts object:", counts);

            const box = document.getElementById("overview-content");

            if (!box) {
                return;
            }

            if (!counts || typeof counts !== "object") {
                box.innerHTML = `<p style="color:red;">Counts failed to load.</p>`;
                return;
            }

            box.innerHTML = `
                <ul>
                    <li><b>Total Files:</b> ${counts.total_files}</li>
                    <li><b>Python Files:</b> ${counts.py_files}</li>
                    <li><b>JS Files:</b> ${counts.js_files}</li>
                    <li><b>HTML Files:</b> ${counts.html_files}</li>
                    <li><b>CSS Files:</b> ${counts.css_files}</li>
                    <li><b>Functions:</b> ${counts.functions}</li>
                    <li><b>Classes:</b> ${counts.classes}</li>
                    <li><b>Methods:</b> ${counts.methods}</li>
                    <li><b>Imports:</b> ${counts.imports}</li>
                    <li><b>Routes:</b> ${counts.routes}</li>
                    <li><b>JS Functions:</b> ${counts.js_functions}</li>
                    <li><b>HTML Events:</b> ${counts.html_events}</li>
                    <li><b>API Calls:</b> ${counts.api_calls}</li>
                </ul>
            `;
        });
}




// ---------------------------------------------------------
// Load all charts (PNG files)
// ---------------------------------------------------------
function loadCharts() {
    fetch(`/dashboard/${PROJECT_NAME}/charts`)
        .then(r => r.json())
        .then(() => {
            // After charts are generated, load them into the DOM
            document.getElementById("chart-file-types").src =
                `/static/projects/${PROJECT_NAME}/file_types.png`;

            document.getElementById("chart-symbols").src =
                `/static/projects/${PROJECT_NAME}/symbol_distribution.png`;

            document.getElementById("chart-routes-js").src =
                `/static/projects/${PROJECT_NAME}/routes_vs_js.png`;

            document.getElementById("chart-api-calls").src =
                `/static/projects/${PROJECT_NAME}/api_calls.png`;

            document.getElementById("chart-html-events").src =
                `/static/projects/${PROJECT_NAME}/html_events.png`;
        });
}
