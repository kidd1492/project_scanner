#core/ir_system/typed_ir/project_ir.py

from dataclasses import dataclass
from typing import List
from .ir_file import IRFile



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


    def get_all_files(self):
        return self.files


    def get_file_by_symbol(self, symbol_id):
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


    def get_calls_of(self, symbol_id):
        symbol = self.find_symbol(symbol_id)
        return symbol.calls if symbol else []


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


    def find_symbols_by_name(self, name):
        return [s for s in self.get_all_symbols() if s.name == name]

  
    def find_symbols_by_file(self, path):
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

    # -------------------------
    # COUNT HELPERS
    # -------------------------

    def count_file_types(self):
        counts = {"py": 0, "js": 0, "html": 0, "css": 0}
        for f in self.files:
            if f.type in counts:
                counts[f.type] += 1
        return counts

    def count_symbols(self):
        total_functions = 0
        total_classes = 0
        total_methods = 0
        total_imports = 0

        for f in self.files:
            total_functions += len(f.functions)
            total_classes += len(f.classes)
            total_imports += len(f.imports)

            for cls in f.classes:
                total_methods += len(cls.methods)

        return {
            "functions": total_functions,
            "classes": total_classes,
            "methods": total_methods,
            "imports": total_imports,
        }

    def count_routes(self):
        return sum(len(f.routes) for f in self.files)

    def count_js_functions(self):
        return sum(len(f.js_functions) for f in self.files)

    def count_html_events(self):
        return sum(len(f.html_events) for f in self.files)

    def count_api_calls(self):
        total = 0
        for f in self.files:
            for jsf in f.js_functions:
                if jsf.api_call:
                    total += 1
        return total

    def summary(self):
        """
        Unified summary used by dashboard + charts.
        """
        file_types = self.count_file_types()
        symbols = self.count_symbols()

        return {
            "total_files": len(self.files),
            "py_files": file_types["py"],
            "js_files": file_types["js"],
            "html_files": file_types["html"],
            "css_files": file_types["css"],
            "functions": symbols["functions"],
            "classes": symbols["classes"],
            "methods": symbols["methods"],
            "imports": symbols["imports"],
            "routes": self.count_routes(),
            "js_functions": self.count_js_functions(),
            "html_events": self.count_html_events(),
            "api_calls": self.count_api_calls(),
        }
