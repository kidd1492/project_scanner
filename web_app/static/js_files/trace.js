document.addEventListener("DOMContentLoaded", () => {
    loadTriggers();
});

function loadTriggers() {
    fetch(`/trace/${PROJECT_NAME}/triggers`)
        .then(r => r.json())
        .then(renderTriggerList)
        .catch(err => console.error("Trigger load error:", err));
}

function renderTriggerList(triggers) {
    const container = document.getElementById("trigger-list");
    container.innerHTML = "";

    const groups = [
        ["JS Functions", triggers.js],
        ["HTML Events", triggers.html],
        ["API Routes", triggers.api],
        ["Python Functions", triggers.python]
    ];

    groups.forEach(([label, items]) => {
        if (!items || items.length === 0) return;

        const section = document.createElement("div");
        section.className = "trigger-section";

        const title = document.createElement("h4");
        title.textContent = label;
        section.appendChild(title);

        items.forEach(item => {
            const btn = document.createElement("button");
            btn.className = "trigger-btn";
            btn.textContent = item;
            btn.onclick = () => runTrace(item);
            section.appendChild(btn);
        });

        container.appendChild(section);
    });
}

function runTrace(trigger) {
    // Load trace tree
    fetch(`/trace/${PROJECT_NAME}/run?trigger=${encodeURIComponent(trigger)}`)
        .then(r => r.json())
        .then(renderTraceTree)
        .catch(err => console.error("Trace error:", err));

    // Load mermaid diagram
    fetch(`/trace/${PROJECT_NAME}/mermaid?trigger=${encodeURIComponent(trigger)}&type=sequence`)
        .then(r => r.json())
        .then(renderMermaid)
        .catch(err => console.error("Mermaid error:", err));
}

function renderTraceTree(tree) {
    const el = document.getElementById("trace-tree");
    el.textContent = JSON.stringify(tree, null, 2);
}

function renderMermaid(data) {
    const el = document.getElementById("mermaid-diagram");
    const code = data.mermaid || "";

    el.innerHTML = `<div class="mermaid">${code}</div>`;
    mermaid.init(undefined, el.querySelectorAll(".mermaid"));
}
