# core/analyzers/ir.py

import os

def build_project_ir(file_types, analyzer_outputs):
    """
    Builds a file-centric IR structure using the new analyzer output schema.
    IR structure:
    {
        "files": [
            {
                "path": "...",
                "source": "...",
                "type": "py|js|html",
                "routes": [...],
                "functions": [...],
                "classes": [...],
                "imports": [...],
                "html_events": [...],
                "js_functions": [...],
                "api_calls": [...]
            }
        ]
    }
    """

    # ---------------------------------------------------------
    # 1. Create a dictionary keyed by file path
    # ---------------------------------------------------------
    files = {}

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
    # 2. Loop through analyzer outputs
    # ---------------------------------------------------------
    for analyzer_output in analyzer_outputs:
        ftype = analyzer_output.get("type")
        results = analyzer_output.get("results")

        # -----------------------------
        # HTML → list of events/scripts
        # -----------------------------
        if ftype == "html":
            for item in results:
                entry = ensure_file_entry(item["file"], "html")

                if item["type"] == "html_event":
                    entry["html_events"].append(item)

                elif item["type"] == "html_script_function":
                    entry["html_events"].append(item)

        # -----------------------------
        # JS → list of JS functions
        # -----------------------------
        elif ftype == "js":
            for item in results:
                entry = ensure_file_entry(item["file"], "js")
                entry["js_functions"].append(item)

                # If fetch() exists, treat it as an API call
                if item.get("api_calls"):
                    entry["api_calls"].append({
                        "name": item["name"],
                        "api_call": item["api_calls"],
                        "file": item["file"],
                        "source": item["source"],
                        "line": item["line"]
                    })

        # -----------------------------
        # PYTHON → dict with lists
        # -----------------------------
        elif ftype == "py":
            # Routes
            for item in results.get("routes", []):
                entry = ensure_file_entry(item["file"], "py")
                entry["routes"].append(item)

            # Functions
            for item in results.get("functions", []):
                entry = ensure_file_entry(item["file"], "py")
                entry["functions"].append(item)

            # Classes
            for item in results.get("classes", []):
                entry = ensure_file_entry(item["file"], "py")
                entry["classes"].append(item)

            # Imports
            for item in results.get("imports", []):
                entry = ensure_file_entry(item["file"], "py")
                entry["imports"].append(item)

    # ---------------------------------------------------------
    # 3. Return IR as a dict
    # ---------------------------------------------------------
    return {
        "files": list(files.values())
    }
