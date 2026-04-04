
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