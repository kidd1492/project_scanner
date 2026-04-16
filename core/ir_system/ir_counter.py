# core/ir_system/ir_counter.py

def compute_ir_counts(ir: dict) -> dict:
    files = ir.get("files", [])

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
        ftype = f.get("type")

        if ftype == "py":
            summary["py_files"] += 1
        elif ftype == "js":
            summary["js_files"] += 1
        elif ftype == "html":
            summary["html_files"] += 1
        elif ftype == "css":
            summary["css_files"] += 1

        summary["functions"] += len(f.get("functions", []))
        summary["classes"] += len(f.get("classes", []))
        summary["imports"] += len(f.get("imports", []))
        summary["routes"] += len(f.get("routes", []))
        summary["js_functions"] += len(f.get("js_functions", []))
        summary["html_events"] += len(f.get("html_events", []))

        # derive API calls from js_functions[*].api_call
        for jsf in f.get("js_functions", []):
            if jsf.get("api_call"):
                summary["api_calls"] += 1

        for cls in f.get("classes", []):
            summary["methods"] += len(cls.get("methods", []))

    return summary
