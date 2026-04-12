document.addEventListener("DOMContentLoaded", () => {
    loadTriggers();
});

function loadTriggers() {
    fetch(`/trace/${PROJECT_NAME}/triggers`)
        .then(r => r.json())
        .then(renderTriggerList);
}

function runTrace(trigger) {
    fetch(`/trace/${PROJECT_NAME}/run?trigger=${trigger}`)
        .then(r => r.json())
        .then(renderTraceTree);

    fetch(`/trace/${PROJECT_NAME}/mermaid?trigger=${trigger}&type=sequence`)
        .then(r => r.json())
        .then(renderMermaid);
}
