function loadAnalysisOnStart() {
    loadAnalysisList("html");
}

function loadAnalysisList(type) {
    fetch(`/analysis/${PROJECT_NAME}/${type}`)
        .then(r => r.json())
        .then(data => {
            const list = document.getElementById("analysis-items");
            list.innerHTML = "";

            data.forEach(item => {
                const funcName = item.function;   // e.g. "chatAsk()"

                const li = document.createElement("li");
                li.className = "analysis-item";
                li.id = funcName;                 // ID = function name
                li.textContent = funcName;

                li.addEventListener("click", () => {
                    runTrace(funcName);
                });

                list.appendChild(li);
            });
        })
        .catch(err => console.error("Error loading analysis list:", err));
}

function runTrace(funcName) {
    const box = document.getElementById("result-window");
    box.innerHTML = `<h3>Tracing: ${funcName}</h3><p>Running trace engine...</p>`;

    const url = `/trace/run?project=${PROJECT_NAME}&trigger=${encodeURIComponent(funcName)}`;
    console.log("FETCHING:", url);

    fetch(url)
        .then(r => r.json())
        .then(trace => {
            box.innerHTML = `<pre>${JSON.stringify(trace, null, 4)}</pre>`;
        })
        .catch(err => {
            box.innerHTML = `<p>Error running trace.</p>`;
            console.error(err);
        });
}
