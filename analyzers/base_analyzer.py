import os, json
from analyzers import html_analyzer, python_analyzer, js_analyzer
from utilities.file_handling import save_python_outputs, save_json

file_type_analyzer_map = {
    "html": html_analyzer,
    "py": python_analyzer,
    "js": js_analyzer
}

def generate_json_reports(file_types, output_dir):
    
    for item in file_types:
        analyzer = file_type_analyzer_map.get(item.get("type"))
        if not analyzer:
            continue

        results = analyzer.analyze_files(item.get("files"))

        # Special handling for Python: split into 3 JSON files
        if item.get("type") == "py":
            save_python_outputs(results, output_dir)
        else:
            output_path = os.path.join(output_dir, f"{item.get("type")}.json")
            save_json(results, output_path)
