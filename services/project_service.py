# services/project_service.py

import os
from core.ir_system.builder import build_project_ir

class ProjectService:
    def __init__(self, typed_ir_cache):
        self.cache = typed_ir_cache

    def get_existing_projects(self):
        if not os.path.exists(self.cache.cache_dir):
            return []
        return [
            name for name in os.listdir(self.cache.cache_dir)
            if os.path.isdir(os.path.join(self.cache.cache_dir, name))
        ]

    def load_project(self, project_name):
        project_ir = self.cache.get(project_name)
        if not project_ir:
            return {"error": "Project not found"}

        return {
            "project_name": project_ir.project_name,
            "total_files": project_ir.total_files,
            "root": project_ir.root,
            "file_types": project_ir.file_types,
        }

    def generate_project_data(self, directory):
        project_ir = build_project_ir(directory)
        self.cache.save(project_ir)

        return {
            "project_name": project_ir.project_name,
            "total_files": project_ir.total_files,
            "root": project_ir.root,
            "file_types": project_ir.file_types,
        }
