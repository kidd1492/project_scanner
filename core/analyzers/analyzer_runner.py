# core/analyzers/analyzer_runner.py

from core.analyzers.base_analyzer import file_type_analyzer_map
from utilities.file_handling import save_analyzer_results

def run_analyzers(file_types, output_dir):
    """
    Runs all analyzers based on file_types and returns a list of:
    {
        "type": "py" | "js" | "html",
        "results": <structured analyzer output>
    }
    """

    final = []

    for item in file_types:
        ftype = item.get("type")
        files = item.get("files", [])

        analyzer = file_type_analyzer_map.get(ftype)
        if not analyzer:
            continue

        results = analyzer.analyze_files(files)

        # Save JSON output for this analyzer
        save_analyzer_results(results, ftype, output_dir)

        final.append({
            "type": ftype,
            "results": results
        })

    return final
