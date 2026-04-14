from core.ir_system.ir_reader import get_file, get_symbol_by_id


class ExplorerService:
    def __init__(self, ir_cache):
        self.ir_cache = ir_cache

    def list_project_files(self, project_name):
        ir = self.ir_cache.get(project_name)["ir"]
        return ir.get("files")

    def get_file_details(self, project_name, path):
        ir = self.ir_cache.get(project_name)["ir"]
        return get_file(ir, path)

    def get_symbol_details(self, project_name, symbol_id):
        ir = self.ir_cache.get(project_name)["ir"]
        return get_symbol_by_id(ir, symbol_id)

    def get_file_source(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
