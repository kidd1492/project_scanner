# services/project_service.py

import os
from utilities.file_handling import open_json
from utilities.file_discovery import discover_files
from core.analyzers.analyzer_runner import run_analyzers
from core.ir_system.ir import build_project_ir
from core.ir_system.ir_writer import save_project_ir


class ProjectService:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir

    # -----------------------------------------
    # List all existing project directories
    # -----------------------------------------
    def get_existing_projects(self):
        projects = []
        if os.path.exists(self.data_dir):
            for name in os.listdir(self.data_dir):
                full_path = os.path.join(self.data_dir, name)
                if os.path.isdir(full_path):
                    projects.append(name)
        return projects

    # -----------------------------------------
    # Load a project's saved metadata + IR
    # -----------------------------------------
    def load_project(self, project_name):
        project_dir = os.path.join(self.data_dir, project_name)
        project_file = os.path.join(project_dir, f"{project_name}.json")

        if not os.path.exists(project_file):
            return f"Project '{project_name}' not found.", 404

        return open_json(project_file)

    # -----------------------------------------
    # Main pipeline: discover → analyze → build IR → save
    # -----------------------------------------
    def generate_project_data(self, directory):
        project_name = os.path.basename(directory)
        project_dir = os.path.join(self.data_dir, project_name)

        if os.path.exists(project_dir):
            return {"results": "Project Exist."}

        self._initialize_project_directory(project_dir)

        file_types, total_files = self._discover_project_files(directory)
        analyzer_outputs = self._run_analysis_pipeline(file_types)
        ir = build_project_ir(analyzer_outputs)

        metadata = {
            "project_name": project_name,
            "total_files": total_files,
            "root": directory,
            "file_types": file_types,
        }

        save_project_ir(project_dir, project_name, ir, metadata)
        return metadata

    # -----------------------------------------
    # Internal helpers
    # -----------------------------------------
    def _initialize_project_directory(self, project_dir):
        os.makedirs(project_dir, exist_ok=True)

    def _discover_project_files(self, directory):
        return discover_files(directory)

    def _run_analysis_pipeline(self, file_types):
        return run_analyzers(file_types)
