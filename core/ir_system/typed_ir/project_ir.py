# core/ir_system/typed_ir/project_ir.py

from dataclasses import dataclass
from typing import List, Optional
from .ir_file import IRFile


@dataclass
class ProjectIR:
    project_name: str
    total_files: int
    root: str
    file_types: list
    files: List[IRFile]

    # -----------------------------------------
    # FILE LOOKUP
    # -----------------------------------------
    def find_file(self, path: str) -> Optional[IRFile]:
        for f in self.files:
            if f.path == path:
                return f
        return None

    def get_all_files(self) -> List[IRFile]:
        return self.files

    # -----------------------------------------
    # SYMBOL LOOKUP
    # -----------------------------------------
    def find_symbol(self, symbol_id: str):
        for f in self.files:
            # functions
            for fn in f.functions:
                if fn.symbol_id == symbol_id:
                    return fn

            # classes + methods
            for cls in f.classes:
                if cls.symbol_id == symbol_id:
                    return cls
                for m in cls.methods:
                    if m.symbol_id == symbol_id:
                        return m

            # routes
            for r in f.routes:
                if r.symbol_id == symbol_id:
                    return r

            # js functions
            for jsf in f.js_functions:
                if jsf.symbol_id == symbol_id:
                    return jsf

            # html events
            for ev in f.html_events:
                if ev.symbol_id == symbol_id:
                    return ev

        return None

    def get_file_by_symbol(self, symbol_id: str) -> Optional[IRFile]:
        for f in self.files:
            # functions
            for fn in f.functions:
                if fn.symbol_id == symbol_id:
                    return f

            # classes + methods
            for cls in f.classes:
                if cls.symbol_id == symbol_id:
                    return f
                for m in cls.methods:
                    if m.symbol_id == symbol_id:
                        return f

            # routes
            for r in f.routes:
                if r.symbol_id == symbol_id:
                    return f

            # js functions
            for jsf in f.js_functions:
                if jsf.symbol_id == symbol_id:
                    return f

            # html events
            for ev in f.html_events:
                if ev.symbol_id == symbol_id:
                    return f

        return None

    # -----------------------------------------
    # SYMBOL COLLECTION
    # -----------------------------------------
    def get_all_symbols(self):
        symbols = []
        for f in self.files:
            symbols.extend(f.functions)
            symbols.extend(f.classes)
            for cls in f.classes:
                symbols.extend(cls.methods)
            symbols.extend(f.routes)
            symbols.extend(f.js_functions)
            symbols.extend(f.html_events)
        return symbols

    def find_symbols_by_name(self, name: str):
        return [s for s in self.get_all_symbols() if s.name == name]

    def find_symbols_by_file(self, path: str):
        f = self.find_file(path)
        if not f:
            return []
        symbols = []
        symbols.extend(f.functions)
        symbols.extend(f.classes)
        for cls in f.classes:
            symbols.extend(cls.methods)
        symbols.extend(f.routes)
        symbols.extend(f.js_functions)
        symbols.extend(f.html_events)
        return symbols

    # -----------------------------------------
    # TRIGGER-LIKE SYMBOLS (routes, js funcs, html events)
    # -----------------------------------------
    def list_triggers(self):
        triggers = []
        for f in self.files:
            triggers.extend(f.routes)
            triggers.extend(f.js_functions)
            triggers.extend(f.html_events)
        return triggers

    # -----------------------------------------
    # ROUTES / JS / EVENTS
    # -----------------------------------------
    def get_routes(self):
        routes = []
        for f in self.files:
            routes.extend(f.routes)
        return routes

    def get_js_functions(self):
        js = []
        for f in self.files:
            js.extend(f.js_functions)
        return js

    def get_html_events(self):
        events = []
        for f in self.files:
            events.extend(f.html_events)
        return events

    # -----------------------------------------
    # SERIALIZATION
    # -----------------------------------------
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
