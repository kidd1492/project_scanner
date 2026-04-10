# services/project_orchestrator.py

import os
from core.ir_system.ir import build_project_ir
from core.ir_system.ir_writer import embed_ir_into_project_json
from services.project_service import initialize_project
from services.ingestion_service import (
    discover_project_files,
    save_project_metadata,
)
from services.analysis_service import run_analysis_pipeline


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


def get_existing_projects():
    DATA_DIR = "data"
    projects = []

    if os.path.exists(DATA_DIR):
        for name in os.listdir(DATA_DIR):
            full_path = os.path.join(DATA_DIR, name)
            if os.path.isdir(full_path):
                projects.append(name)
    return projects
