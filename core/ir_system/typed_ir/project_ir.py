from dataclasses import dataclass, field
from typing import List, Optional
from .typed_ir import IRFile

# -------------------------
# PROJECT IR
# -------------------------

@dataclass
class ProjectIR:
    project_name: str
    total_files: int
    root: str
    file_types: list
    files: List[IRFile]

    def find_file(self, path):
        for f in self.files:
            if f.path == path:
                return f
        return None

    def find_symbol(self, symbol_id):
        for f in self.files:
            for fn in f.functions:
                if fn.symbol_id == symbol_id:
                    return fn
            for cls in f.classes:
                if cls.symbol_id == symbol_id:
                    return cls
                for m in cls.methods:
                    if m.symbol_id == symbol_id:
                        return m
            for r in f.routes:
                if r.symbol_id == symbol_id:
                    return r
            for jsf in f.js_functions:
                if jsf.symbol_id == symbol_id:
                    return jsf
            for ev in f.html_events:
                if ev.symbol_id == symbol_id:
                    return ev
        return None

    def list_triggers(self):
        triggers = []
        for f in self.files:
            triggers.extend(f.routes)
            triggers.extend(f.js_functions)
            triggers.extend(f.html_events)
        return triggers


    def to_dict(self):
        return {
            "project_name": self.project_name,
            "total_files": self.total_files,
            "root": self.root,
            "file_types": self.file_types,
            "files": [f.to_dict() for f in self.files],
        }

    @staticmethod
    def from_dict(d):
        return ProjectIR(
            project_name=d["project_name"],
            total_files=d["total_files"],
            root=d["root"],
            file_types=d["file_types"],
            files=[IRFile.from_dict(f) for f in d["files"]],
        )
