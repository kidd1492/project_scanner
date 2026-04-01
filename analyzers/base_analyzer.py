import os, json
from analyzers import html_analyzer, python_analyzer, js_analyzer
from .helpers import analyze_project, save_json

file_type_analyzer_map = {
    "html": html_analyzer,
    "py": python_analyzer,
    "js": js_analyzer
}

def generate_json_reports(directory: str, output_dir="data"):
    data = analyze_project(directory)
    categorized = data.get("file_types")

    for item in categorized:
        analyzer = file_type_analyzer_map.get(item.get("type"))
        if not analyzer:
            continue

        results = analyzer.analyze_files(item.get("files"))

        # Special handling for Python: split into 3 JSON files
        if item.get("type") == "py":
            save_python_outputs(results, output_dir)
        else:
            output_path = os.path.join(output_dir, f"{item.get("type")}.json")
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=4)


def save_python_outputs(results, output_dir):
    """Save API, classes, and functions as separate JSON files."""
    api_path = os.path.join(output_dir, "api.json")
    classes_path = os.path.join(output_dir, "classes.json")
    functions_path = os.path.join(output_dir, "functions.json")

    with open(api_path, "w", encoding="utf-8") as f:
        json.dump(results["routes"], f, indent=4)

    with open(classes_path, "w", encoding="utf-8") as f:
        json.dump(results["classes"], f, indent=4)

    with open(functions_path, "w", encoding="utf-8") as f:
        json.dump(results["functions"], f, indent=4)
