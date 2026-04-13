# services/project_orchestrator.py
from utilities.file_handling import save_json
from utilities.file_discovery import discover_files
from core.analyzers.analyzer_runner import run_analyzers
from core.ir_system.ir import build_project_ir
from core.ir_system.ir_writer import embed_ir_into_project_json
import os


def scan_project_files(directory: str):

    project_name = os.path.basename(directory)
    project_dir = f"data/{project_name}"
    if _project_exists(project_dir):
        return {"results": "Project Exist."}
    
    _initialize_project_directory(project_dir)

    # 1. Discover files
    file_types, total_files = discover_project_files(directory)

    # 2. Run analyzers
    analyzer_outputs = run_analysis_pipeline(file_types, project_dir)

    # 3. Save metadata
    metadata = save_project_metadata(
        project_name=project_name,
        root_dir=directory,
        file_types=file_types,
        total_files=total_files,
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
    }

    save_json(metadata, f"{project_dir}/{project_name}.json")
    save_json({"last": project_name}, "data/last_project.json")

    return metadata


def _project_exists(project_dir: str) -> bool:
    return os.path.exists(project_dir)


def _initialize_project_directory(project_dir: str):
    os.makedirs(project_dir, exist_ok=True)


def run_analysis_pipeline(file_types, project_dir):
    """
    Runs all analyzers, saves their JSON outputs, and returns:
    - analysis_counts: summary counts for dashboard
    - analyzer_outputs: raw analyzer results for IR builder
    """

    analyzer_outputs = run_analyzers(file_types, project_dir)
    return analyzer_outputs


def save_project_metadata(
    project_name: str,
    root_dir: str,
    file_types,
    total_files: int,
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
    }

    save_json(metadata, f"{project_dir}/{project_name}.json")
    save_json({"last": project_name}, "data/last_project.json")

    return metadata