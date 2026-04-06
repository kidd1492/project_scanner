import os
from utilities.file_handling import save_json, open_json
from utilities.file_discovery import discover_files
from utilities import chart_generator
from analyzers.base_analyzer import generate_json_reports


def ingest_project(directory: str):
    """
    Orchestrates the full ingestion pipeline:
    - project directory setup
    - file discovery
    - analysis execution
    - persistence
    - visualization
    - metadata saving
    """
    project_name = os.path.basename(directory)
    project_dir = f"data/{project_name}"

    if _project_exists(project_dir):
        return _handle_existing_project(project_name)

    _initialize_project_directory(project_dir)
    file_types, total_files = _discover_project_files(directory)
    analysis_counts = _run_analysis_pipeline(file_types, project_dir, project_name)
    metadata = _save_project_metadata(project_name, directory, file_types, total_files, analysis_counts)

    return metadata


# ---------------------------------------------------------
# Internal helpers — explicit, testable, single‑purpose
# ---------------------------------------------------------

def _project_exists(project_dir: str) -> bool:
    return os.path.exists(project_dir)


def _handle_existing_project(project_name: str):
    save_json({"last": project_name}, "data/last_project.json")
    return {"results": "Project Exist."}


def _initialize_project_directory(project_dir: str):
    os.makedirs(project_dir, exist_ok=True)


def _discover_project_files(directory: str):
    """Returns (file_types, total_files)."""
    return discover_files(directory)


def _run_analysis_pipeline(file_types, project_dir, project_name):
    """Runs analyzers, writes JSON outputs, generates charts, returns summary counts."""
    results = generate_json_reports(file_types, project_dir)
    analysis_counts = get_counts(results)

    chart_generator.file_pie_chat(file_types, project_name)
    chart_generator.analysis_bar_chart(analysis_counts, project_name)

    return analysis_counts


def _save_project_metadata(project_name, root_dir, file_types, total_files, analysis_counts):
    """Persists the project metadata JSON and updates last_project.json."""
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



def get_existing_projects():
    DATA_DIR = "data"
    projects = []

    if os.path.exists(DATA_DIR):
        for name in os.listdir(DATA_DIR):
            full_path = os.path.join(DATA_DIR, name)
            if os.path.isdir(full_path):
                projects.append(name)
    return projects


def get_counts(results):
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

        # PYTHON → dict with 3 lists
        elif analyzer_type == "py":
            summary["api_routes"] = len(analyzer_results.get("routes", []))
            summary["classes"] = len(analyzer_results.get("classes", []))
            summary["python_functions"] = len(analyzer_results.get("functions", []))

    return summary


