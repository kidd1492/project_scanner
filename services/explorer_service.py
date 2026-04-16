# services/explorer_service.py

class ExplorerService:
    def __init__(self, ir_cache):
        self.ir_cache = ir_cache

    def list_project_files(self, project_name):
        project_ir = self.ir_cache.load(project_name)
        return project_ir["files"]

    def get_file_details(self, project_name, path):
        project_ir = self.ir_cache.load(project_name)
        for f in project_ir["files"]:
            if f["path"] == path:
                return f
        return None

    def get_symbol_details(self, project_name, symbol_id):
        project_ir = self.ir_cache.load(project_name)

        for f in project_ir["files"]:
            # functions
            for fn in f.get("functions", []):
                if fn["symbol_id"] == symbol_id:
                    return fn

            # classes + methods
            for cls in f.get("classes", []):
                if cls["symbol_id"] == symbol_id:
                    return cls
                for m in cls.get("methods", []):
                    if m["symbol_id"] == symbol_id:
                        return m

            # routes
            for r in f.get("routes", []):
                if r["symbol_id"] == symbol_id:
                    return r

            # js functions
            for jsf in f.get("js_functions", []):
                if jsf["symbol_id"] == symbol_id:
                    return jsf

            # html events
            for ev in f.get("html_events", []):
                if ev["symbol_id"] == symbol_id:
                    return ev

        return None

    def get_file_source(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
