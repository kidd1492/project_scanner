def compute_ir_counts(project_ir) -> dict:
    """
    Strict typed‑IR version.
    Expects a ProjectIR instance.
    """

    files = project_ir.files  # List[IRFile]

    summary = {
        "total_files": len(files),
        "py_files": 0,
        "js_files": 0,
        "html_files": 0,
        "css_files": 0,
        "functions": 0,
        "classes": 0,
        "methods": 0,
        "imports": 0,
        "routes": 0,
        "js_functions": 0,
        "html_events": 0,
        "api_calls": 0,
    }

    for f in files:
        ftype = f.type

        if ftype == "py":
            summary["py_files"] += 1
        elif ftype == "js":
            summary["js_files"] += 1
        elif ftype == "html":
            summary["html_files"] += 1
        elif ftype == "css":
            summary["css_files"] += 1

        summary["functions"] += len(f.functions)
        summary["classes"] += len(f.classes)
        summary["imports"] += len(f.imports)
        summary["routes"] += len(f.routes)
        summary["js_functions"] += len(f.js_functions)
        summary["html_events"] += len(f.html_events)

        # derive API calls from js_functions[*].api_call
        for jsf in f.js_functions:
            if jsf.api_call:
                summary["api_calls"] += 1

        for cls in f.classes:
            summary["methods"] += len(cls.methods)

    return summary
