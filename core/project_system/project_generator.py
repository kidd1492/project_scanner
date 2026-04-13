# services/project_orchestrator.py
from utilities.file_discovery import discover_files
from core.analyzers.analyzer_runner import run_analyzers
from core.ir_system.ir import build_project_ir
from core.ir_system.ir_writer import save_project_ir
import os


def scan_project_files(directory: str):

    project_name = os.path.basename(directory)
    project_dir = f"data/{project_name}"
    if os.path.exists(project_dir):
        return {"results": "Project Exist."}
    
    _initialize_project_directory(project_dir)

    # 1. Discover files
    file_types, total_files = discover_project_files(directory)

    # 2. Run analyzers
    analyzer_outputs = run_analysis_pipeline(file_types)
    ir = build_project_ir(analyzer_outputs)

    metadata = {
        "project_name": project_name,
        "total_files": total_files,
        "root": directory,
        "file_types": file_types,
    }

    save_project_ir(project_dir, project_name, ir, metadata)
    return metadata


def discover_project_files(directory: str):
    """
    Returns (file_types, total_files) for a given project root.
    """
    return discover_files(directory)


def _initialize_project_directory(project_dir: str):
    os.makedirs(project_dir, exist_ok=True)


def run_analysis_pipeline(file_types):
    """
    Runs all analyzers, returns:
    - analysis_counts: summary counts for dashboard
    - analyzer_outputs: raw analyzer results for IR builder
    """

    analyzer_outputs = run_analyzers(file_types)
    return analyzer_outputs
