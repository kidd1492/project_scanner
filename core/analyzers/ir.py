import json

def build_project_ir(file_types, analyzer_outputs, project_dir, project_name):
    # 1. Build file index
    files = {}
    for ft in file_types:
        for f in ft["files"]:
            files[f] = {
                "path": f,
                "type": ft["type"],
                "html_events": [],
                "js_functions": [],
                "api_calls": [],
                "routes": [],
                "classes": [],
                "functions": []
            }

    # 2. Merge analyzer outputs
    for block in analyzer_outputs:
        atype = block["type"]
        results = block["results"]

        if atype == "html":
            for item in results:
                files[item["file"]]["html_events"].append(item)

        elif atype == "js":
            for item in results:
                files[item["file"]]["js_functions"].append(item)
                if item.get("api_calls"):
                    files[item["file"]]["api_calls"].append(item["api_calls"])

        elif atype == "py":
            for route in results.get("routes", []):
                files[route["file"]]["routes"].append(route)

            for cls in results.get("classes", []):
                files[cls["file"]]["classes"].append(cls)

            for func in results.get("functions", []):
                files[func["file"]]["functions"].append(func)

    # 3. Build final IR
    ir = {
        "project": {
            "name": project_name,
            "root": project_dir,
            "total_files": len(files)
        },
        "files": list(files.values())
    }

    # 4. Save IR
    output_path = f"{project_dir}/ir.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(ir, f, indent=4)

    return ir
