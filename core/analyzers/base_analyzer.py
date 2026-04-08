import os, json
from core.analyzers import python_analyzer
from core.analyzers import html_analyzer, js_analyzer
from utilities.file_handling import save_analyzer_results

file_type_analyzer_map = {
    "html": html_analyzer,
    "py": python_analyzer,
    "js": js_analyzer
}

def generate_json_reports(file_types, output_dir):
    final = []
    for item in file_types:
        type = item.get("type")
        analyzer = file_type_analyzer_map.get(type)
        if not analyzer:
            continue

        results = analyzer.analyze_files(item.get("files"))
        final.append({"type": type, "results":results})
        save_analyzer_results(results, type, output_dir)
    return final

