# services/project_service.py

import os
from utilities.file_handling import open_json
from core.ir_system.builder import build_project_ir
from core.ir_system.ir_writer import save_project_ir


class ProjectService:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir

    def get_existing_projects(self):
        projects = []
        if os.path.exists(self.data_dir):
            for name in os.listdir(self.data_dir):
                full_path = os.path.join(self.data_dir, name)
                if os.path.isdir(full_path):
                    projects.append(name)
        return projects

    def load_project(self, project_name):
        project_dir = os.path.join(self.data_dir, project_name)
        project_file = os.path.join(project_dir, f"{project_name}.json")

        if not os.path.exists(project_file):
            return f"Project '{project_name}' not found.", 404

        return open_json(project_file)

    # NEW TYPED-IR PIPELINE
    def generate_project_data(self, directory):
        project_name = os.path.basename(directory)
        project_dir = os.path.join(self.data_dir, project_name)

        if os.path.exists(project_dir):
            return {"results": "Project Exist."}

        os.makedirs(project_dir, exist_ok=True)

        project_ir = build_project_ir(directory)

        metadata = {
            "project_name": project_ir.project_name,
            "total_files": project_ir.total_files,
            "root": project_ir.root,
            "file_types": project_ir.file_types,
        }

        save_project_ir(project_dir, project_name, project_ir.to_dict(), metadata)

        return metadata
