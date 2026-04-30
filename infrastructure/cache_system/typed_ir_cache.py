# infrastructure/cache_system/typed_ir_cache.py

import os
from project_domain.project_ir import ProjectIR

class TypedIRCache:
    """Environment-dependent persistence tool for ProjectIR.
    Uses FileReader for all I/O. Swappable. Injectable. CAP‑aligned."""

    def __init__(self, cache_dir="cache", file_reader=None):
        self.cache_dir = cache_dir
        self.file_reader = file_reader  # injected tool
        self._cache = {}

        os.makedirs(self.cache_dir, exist_ok=True)

    def preload_all(self):
        print(f"\n\npreload\n\n")
        for project_name in os.listdir(self.cache_dir):
            project_dir = os.path.join(self.cache_dir, project_name)
            project_file = os.path.join(project_dir, f"{project_name}.json")

            if os.path.exists(project_file):
                data = self.file_reader.read_json(project_file)
                self._cache[project_name] = ProjectIR.from_dict(data)

    def load(self, project_name):
        # in-memory cache hit
        if project_name in self._cache:
            return self._cache[project_name]

        # fallback to disk
        project_dir = os.path.join(self.cache_dir, project_name)
        project_file = os.path.join(project_dir, "project.json")

        if not os.path.exists(project_file):
            return None

        data = self.file_reader.read_json(project_file)
        project_ir = ProjectIR.from_dict(data)
        self._cache[project_name] = project_ir
        return project_ir

    def save(self, project_ir: ProjectIR):
        project_name = project_ir.project_name
        project_dir = os.path.join(self.cache_dir, project_name)
        os.makedirs(project_dir, exist_ok=True)

        project_file = os.path.join(project_dir, "project.json")
        self.file_reader.write_json(project_file, project_ir.to_dict())

        self._cache[project_name] = project_ir

    def get(self, project_name):
        return self._cache.get(project_name)
