# infrastructure/ir_cache.py
from typing import Dict, Any
from core.ir_system.typed_ir_adapter import project_ir_from_dict
from core.ir_system.typed_ir import ProjectIR

class IRCache:
    def __init__(self, loader):
        self.loader = loader
        self._cache = {}
        self._typed_cache = {}   #separate cache for typed IR


    def get(self, project_name):
        if project_name not in self._cache:
            self._cache[project_name] = self.loader(project_name)
        return self._cache[project_name]


    def invalidate(self, project_name):
        self._cache.pop(project_name, None)
        self._typed_cache.pop(project_name, None)  #clear typed cache

    def get_raw(self, project_name) -> Dict[str, Any]:
        return self.get(project_name)

    def get_typed(self, project_name) -> ProjectIR:
        if project_name not in self._typed_cache:
            raw = self.get(project_name)
            ir_dict = raw.get("ir", raw)
            self._typed_cache[project_name] = project_ir_from_dict(ir_dict)
        return self._typed_cache[project_name]
