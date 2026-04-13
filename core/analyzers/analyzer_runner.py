# core/analyzers/analyzer_runner.py

from core.analyzers.base_analyzer import file_type_analyzer_map


def run_analyzers(file_types):
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

        final.append({
            "type": ftype,
            "results": results
        })

    return final
