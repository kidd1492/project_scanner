# infrastructure/ir_cache.py

import os
from utilities.file_handling import open_json

class IRCache:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir

    def load(self, project_name):
        project_dir = os.path.join(self.data_dir, project_name)
        project_file = os.path.join(project_dir, f"{project_name}.json")

        if not os.path.exists(project_file):
            return None

        return open_json(project_file)

    def exists(self, project_name):
        project_dir = os.path.join(self.data_dir, project_name)
        project_file = os.path.join(project_dir, f"{project_name}.json")
        return os.path.exists(project_file)

# infrastructure/typed_ir_cache.py
import json
from core.ir_system.typed_ir import ProjectIR

class TypedIRCache:
    def __init__(self, cache_dir="cache"):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def load(self, project_name) -> ProjectIR | None:
        project_dir = os.path.join(self.cache_dir, project_name)
        project_file = os.path.join(project_dir, "project.json")

        if not os.path.exists(project_file):
            return None

        data = open_json(project_file)
        return ProjectIR.from_dict(data)

    def save(self, project_ir: ProjectIR):
        project_name = project_ir.project_name
        project_dir = os.path.join(self.cache_dir, project_name)
        os.makedirs(project_dir, exist_ok=True)

        project_file = os.path.join(project_dir, "project.json")
        with open(project_file, "w", encoding="utf-8") as f:
            json.dump(project_ir.to_dict(), f, indent=2)

        