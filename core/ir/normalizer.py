# core/ir/normalizer.py

import json
from pathlib import Path
from .schema import ProjectIR
from .merger import (
    ensure_file_entry,
    merge_trigger,
    merge_js_function,
    merge_api_call,
    merge_route,
    merge_class,
    merge_python_function,
    normalize_path,
)

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def detect_language(path: str) -> str:
    ext = Path(path).suffix.lower()
    return {
        ".py": "python",
        ".js": "javascript",
        ".html": "html",
        ".htm": "html",
        ".css": "css",
        ".md": "markdown",
    }.get(ext, "unknown")


def infer_kind(path: str) -> str:
    if "templates" in path:
        return "template"
    if "static" in path:
        return "asset"
    return "source"


def build_ir(project_dir: str):
    """
    Build a unified IR from the existing JSON outputs.
    project_dir = data/<project_name>
    """

    project_json = load_json(Path(project_dir) / "project_scanner.json")
    html_json = load_json(Path(project_dir) / "html.json")
    js_json = load_json(Path(project_dir) / "js.json")
    api_json = load_json(Path(project_dir) / "api.json")
    classes_json = load_json(Path(project_dir) / "classes.json")
    functions_json = load_json(Path(project_dir) / "functions.json")

    ir = {
        "project": {
            "name": project_json["project_name"],
            "root": normalize_path(project_json["root"]),
            "file_types": project_json["file_types"],
            "analysis_counts": project_json["analysis_counts"],
        },
        "files": [],
    }

    # ------------------------------------------------------------
    # 1. Initialize file entries from project_scanner.json
    # ------------------------------------------------------------
    for ft in project_json["file_types"]:
        for file_path in ft["files"]:
            file_path = normalize_path(file_path)
            language = detect_language(file_path)
            kind = infer_kind(file_path)
            ensure_file_entry(ir, file_path, language, kind)

    # ------------------------------------------------------------
    # 2. HTML triggers → IR["files"][i]["triggers"]
    # ------------------------------------------------------------
    for trig in html_json:
        file_entry = ensure_file_entry(
            ir,
            trig["file"],
            detect_language(trig["file"]),
            infer_kind(trig["file"]),
        )

        merge_trigger(file_entry, {
            "type": "dom_event",
            "event": trig.get("event"),
            "selector": None,
            "handler": trig.get("function").replace("(", "").replace(")", ""),
            "file": normalize_path(trig["file"]),
        })

    # ------------------------------------------------------------
    # 3. JS functions + API calls
    # ------------------------------------------------------------
    for js in js_json:
        file_entry = ensure_file_entry(
            ir,
            js["file"],
            "javascript",
            infer_kind(js["file"]),
        )

        func_name = js["function"].replace("(", "").replace(")", "")

        merge_js_function(file_entry, {
            "name": func_name,
            "qualified_name": func_name,
            "lineno": None,
            "end_lineno": None,
            "calls": [],
            "is_route_handler": False,
            "route": None,
            "http_methods": None,
            "returns": None,
        })

        if js.get("api_calls"):
            merge_api_call(file_entry, {
                "raw": js["api_calls"],
                "normalized_path": None,  # filled later by trace engine
                "method": "GET",
                "file": normalize_path(js["file"]),
                "function": func_name,
                "lineno": None,
            })

    # ------------------------------------------------------------
    # 4. API routes + Python route handlers
    # ------------------------------------------------------------
    for api in api_json:
        file_entry = ensure_file_entry(
            ir,
            api["file"],
            "python",
            infer_kind(api["file"]),
        )

        merge_route(file_entry, {
            "route": api["route"],
            "function": api["function"],
            "file": normalize_path(api["file"]),
            "http_methods": ["GET"],  # default
        })

        merge_python_function(file_entry, {
            "name": api["function"],
            "qualified_name": api["function"],
            "lineno": None,
            "end_lineno": None,
            "calls": api.get("calls", []),
            "is_route_handler": True,
            "route": api["route"],
            "http_methods": ["GET"],
            "returns": api.get("returns"),
        })

    # ------------------------------------------------------------
    # 5. Classes.json → IR["files"][i]["classes"]
    # ------------------------------------------------------------
    for cls in classes_json:
        file_entry = ensure_file_entry(
            ir,
            cls["file"],
            "python",
            infer_kind(cls["file"]),
        )

        merge_class(file_entry, {
            "name": cls["class"],
            "qualified_name": cls["class"],
            "lineno": None,
            "methods": [m["method"] for m in cls["methods"]],
        })

    # ------------------------------------------------------------
    # 6. functions.json → IR["files"][i]["functions"]
    # ------------------------------------------------------------
    for fn in functions_json:
        file_entry = ensure_file_entry(
            ir,
            fn["file"],
            "python",
            infer_kind(fn["file"]),
        )

        merge_python_function(file_entry, {
            "name": fn["function"],
            "qualified_name": fn["function"],
            "lineno": None,
            "end_lineno": None,
            "calls": fn.get("calls", []),
            "is_route_handler": False,
            "route": None,
            "http_methods": None,
            "returns": fn.get("returns"),
        })

    # ------------------------------------------------------------
    # 7. Write IR to disk
    # ------------------------------------------------------------
    out_path = Path(project_dir) / "ir.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(ir, f, indent=4)

    return ir
