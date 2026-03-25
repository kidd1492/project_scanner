import os
import json
from analyzers import html_analyzer, python_analyzer, js_analyzer

file_type_analyzer_map = {
    "html": html_analyzer,
    "py": python_analyzer,
    "js": js_analyzer
}

def generate_json_reports(directory: str, output_dir="data"):
    os.makedirs(output_dir, exist_ok=True)
    categorized = gather_categorized_files(directory)

    for file_type, file_list in categorized.items():
        analyzer = file_type_analyzer_map.get(file_type)
        if not analyzer:
            continue

        results = analyzer.analyze_files(file_list)

        # Special handling for Python: split into 3 JSON files
        if file_type == "py":
            save_python_outputs(results, output_dir)
        else:
            output_path = os.path.join(output_dir, f"{file_type}.json")
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


def gather_categorized_files(directory):
    allowed_extensions = [".py", ".html", ".js"]
    ignored_directories = [".git", "env", "venv"]

    categorized = {}

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ignored_directories]

        for file in files:
            if any(file.endswith(ext) for ext in allowed_extensions):
                ext = file.split('.')[-1]
                categorized.setdefault(ext, []).append(
                    os.path.join(root, file)
                )

    return categorized
