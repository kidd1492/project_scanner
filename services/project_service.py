# services/project_service.py

import os
from core.ir_system.builder import build_project_ir

class ProjectService:
    def __init__(self, typed_ir_cache):
        self.cache = typed_ir_cache

    #
    # PROJECT DISCOVERY
    #
    def get_existing_projects(self):
        if not os.path.exists(self.cache.cache_dir):
            return []
        return [
            name
            for name in os.listdir(self.cache.cache_dir)
            if os.path.isdir(os.path.join(self.cache.cache_dir, name))
        ]

    #
    # LOAD FULL PROJECT IR
    #
    def load_project(self, project_name):
        return self.cache.get(project_name)

    #
    # BUILD + SAVE PROJECT IR
    #
    def generate_project_data(self, directory):
        project_ir = build_project_ir(directory)
        self.cache.save(project_ir)
        return project_ir

    #
    # DOMAIN OPERATIONS (delegated to ProjectIR)
    #
    def get_summary(self, project_name):
        project = self.cache.get(project_name)
        return project.summary() if project else None

    def get_files(self, project_name):
        project = self.cache.get(project_name)
        return project.get_all_files() if project else None

    def get_symbols(self, project_name):
        project = self.cache.get(project_name)
        return project.get_all_symbols() if project else None

    def get_routes(self, project_name):
        project = self.cache.get(project_name)
        return project.get_routes() if project else None
