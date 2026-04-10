# services/analysis_service.py

from core.analyzers.analyzer_runner import run_analyzers
from core.chart_system import chart_generator


def run_analysis_pipeline(file_types, project_dir, project_name):
    """
    Runs all analyzers, saves their JSON outputs, and returns:
    - analysis_counts: summary counts for dashboard
    - analyzer_outputs: raw analyzer results for IR builder
    """

    analyzer_outputs = run_analyzers(file_types, project_dir)
    analysis_counts = get_analysis_counts(analyzer_outputs)

    # Generate charts
    chart_generator.file_pie_chat(file_types, project_name)
    chart_generator.analysis_bar_chart(analysis_counts, project_name)

    return analysis_counts, analyzer_outputs


def get_analysis_counts(results):
    """
    Takes the in-memory analyzer results list and returns a summary count dict.
    """

    summary = {
        "html_triggers": 0,
        "js_functions": 0,
        "api_routes": 0,
        "classes": 0,
        "python_functions": 0
    }

    for item in results:
        analyzer_type = item.get("type")
        analyzer_results = item.get("results", [])

        # HTML → list
        if analyzer_type == "html":
            summary["html_triggers"] = len(analyzer_results)

        # JS → list
        elif analyzer_type == "js":
            summary["js_functions"] = len(analyzer_results)

        # PYTHON → dict with lists
        elif analyzer_type == "py":
            summary["api_routes"] = len(analyzer_results.get("routes", []))
            summary["classes"] = len(analyzer_results.get("classes", []))
            summary["python_functions"] = len(analyzer_results.get("functions", []))

    return summary
