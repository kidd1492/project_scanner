# services/project_orchestrator.py
from utilities.file_handling import save_json
from utilities.file_discovery import discover_files
from core.analyzers.analyzer_runner import run_analyzers
from core.chart_system import chart_generator
from core.ir_system.ir import build_project_ir
from core.ir_system.ir_writer import embed_ir_into_project_json
from services.project_service import initialize_project



def scan_project_files(directory: str):
    init = initialize_project(directory)

    if init["results"] == "Project Exist.":
        return init

    project_name = init["project_name"]
    project_dir = init["project_dir"]

    # 1. Discover files
    file_types, total_files = discover_project_files(directory)

    # 2. Run analyzers
    analysis_counts, analyzer_outputs = run_analysis_pipeline(
        file_types, project_dir, project_name
    )

    # 3. Save metadata
    metadata = save_project_metadata(
        project_name=project_name,
        root_dir=directory,
        file_types=file_types,
        total_files=total_files,
        analysis_counts=analysis_counts,
    )

    # 4. Build IR
    ir = build_project_ir(file_types, analyzer_outputs)

    # 5. Embed IR into project.json
    embed_ir_into_project_json(project_dir, project_name, ir)

    return metadata


def discover_project_files(directory: str):
    """
    Returns (file_types, total_files) for a given project root.
    """
    return discover_files(directory)


def save_project_metadata(
    project_name: str,
    root_dir: str,
    file_types,
    total_files: int,
    analysis_counts: dict
):
    """
    Persists the project metadata JSON and updates last_project.json.
    """
    project_dir = f"data/{project_name}"
    metadata = {
        "project_name": project_name,
        "total_files": total_files,
        "root": root_dir,
        "file_types": file_types,
        "analysis_counts": analysis_counts,
    }

    save_json(metadata, f"{project_dir}/{project_name}.json")
    save_json({"last": project_name}, "data/last_project.json")

    return metadata


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


def save_project_metadata(
    project_name: str,
    root_dir: str,
    file_types,
    total_files: int,
    analysis_counts: dict
):
    """
    Persists the project metadata JSON and updates last_project.json.
    """
    project_dir = f"data/{project_name}"
    metadata = {
        "project_name": project_name,
        "total_files": total_files,
        "root": root_dir,
        "file_types": file_types,
        "analysis_counts": analysis_counts,
    }

    save_json(metadata, f"{project_dir}/{project_name}.json")
    save_json({"last": project_name}, "data/last_project.json")

    return metadata