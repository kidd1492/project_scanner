import os
from utilities.file_handling import save_json

# services/project_orchestrator.py

from services.project_service import initialize_project
from services.ingestion_service import (
    discover_project_files,
    save_project_metadata,
    build_project_ir,
)
from services.analysis_service import run_analysis_pipeline


def scan_project(directory: str):
    """
    High-level orchestration for scanning a project:
      1. Initialize project
      2. Discover files
      3. Run analyzers
      4. Save metadata
      5. Build IR
    """
    init = initialize_project(directory)

    # If project already exists, just return that info
    if init["results"] == "Project Exist.":
        return init

    project_name = init["project_name"]
    project_dir = init["project_dir"]

    # 1. Discover files
    file_types, total_files = discover_project_files(directory)

    # 2. Run analyzers
    analysis_counts = run_analysis_pipeline(file_types, project_dir, project_name)

    # 3. Save metadata
    metadata = save_project_metadata(
        project_name=project_name,
        root_dir=directory,
        file_types=file_types,
        total_files=total_files,
        analysis_counts=analysis_counts,
    )

    # 4. Build IR (optional to make this toggleable later)
    #build_project_ir(project_dir)

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