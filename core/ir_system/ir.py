# core/analyzers/ir.py

import os

# ---------------------------------------------------------
# Helper: generate short, stable symbol IDs
# Format: <folder>/<source>::<symbol_name>
# Example: api/dashboard_routes.py::dashboard
# ---------------------------------------------------------
def make_symbol_id(path, name):
    norm = path.replace("\\", "/")
    parts = norm.split("/")
    if len(parts) >= 2:
        folder = parts[-2]
        source = parts[-1]
        return f"{folder}/{source}::{name}"
    else:
        # fallback (should never happen)
        return f"{parts[-1]}::{name}"


def build_project_ir(analyzer_outputs):
    """
    Builds a file-centric IR structure using the new analyzer output schema.
    """
    files = {}

    # ---------------------------------------------------------
    # Ensure file entry exists
    # ---------------------------------------------------------
    def ensure_file_entry(path, ftype):
        path = path.replace("\\", "/")
        if path not in files:
            files[path] = {
                "path": path,
                "source": os.path.basename(path),
                "type": ftype,
                "routes": [],
                "functions": [],
                "classes": [],
                "imports": [],
                "html_events": [],
                "js_functions": [],
                "api_calls": []
            }
        return files[path]

    # ---------------------------------------------------------
    # Process analyzer outputs
    # ---------------------------------------------------------
    for analyzer_output in analyzer_outputs:
        ftype = analyzer_output.get("type")
        results = analyzer_output.get("results")

        # -----------------------------
        # HTML
        # -----------------------------
        if ftype == "html":
            for item in results:
                entry = ensure_file_entry(item["file"], "html")

                # Add symbol_id
                item["symbol_id"] = make_symbol_id(item["file"], item["name"])

                if item["type"] in ("html_event", "html_script_function"):
                    entry["html_events"].append(item)

        # -----------------------------
        # JS
        # -----------------------------
        elif ftype == "js":
            for item in results:
                entry = ensure_file_entry(item["file"], "js")

                # Add symbol_id
                item["symbol_id"] = make_symbol_id(item["file"], item["name"])

                entry["js_functions"].append(item)

                # API calls inside JS
                if item.get("api_calls"):
                    entry["api_calls"].append({
                        "name": item["name"],
                        "symbol_id": item["symbol_id"],
                        "api_call": item["api_calls"],
                        "file": item["file"],
                        "source": item["source"],
                        "line": item["line"]
                    })

        # -----------------------------
        # PYTHON
        # -----------------------------
        elif ftype == "py":

            # Routes
            for item in results.get("routes", []):
                entry = ensure_file_entry(item["file"], "py")
                item["symbol_id"] = make_symbol_id(item["file"], item["name"])
                entry["routes"].append(item)

            # Functions
            for item in results.get("functions", []):
                entry = ensure_file_entry(item["file"], "py")
                item["symbol_id"] = make_symbol_id(item["file"], item["name"])
                entry["functions"].append(item)

            # Classes
            for item in results.get("classes", []):
                entry = ensure_file_entry(item["file"], "py")
                item["symbol_id"] = make_symbol_id(item["file"], item["name"])

                # Add symbol IDs to methods if present
                if "methods" in item:
                    for m in item["methods"]:
                        m["symbol_id"] = make_symbol_id(
                            item["file"],
                            f"{item['name']}.{m['name']}"
                        )

                entry["classes"].append(item)

            # Imports
            for item in results.get("imports", []):
                entry = ensure_file_entry(item["file"], "py")
                entry["imports"].append(item)

    # ---------------------------------------------------------
    # Return IR
    # ---------------------------------------------------------
    return {
        "files": list(files.values())
    }
