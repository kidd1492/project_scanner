# services/explorer_service.py

class ExplorerService:
    def __init__(self, typed_ir_cache):
        #self.ir_cache = ir_cache
        self.typed_ir_cache = typed_ir_cache  # typed IR


    def get_file_source(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()


    def list_project_files(self, project_name):
        project_ir = self.typed_ir_cache.load(project_name)
        return [f.to_dict() for f in project_ir.files]

    
    def get_file_details(self, project_name, path):
        project_ir = self.typed_ir_cache.load(project_name)
        file = project_ir.find_file(path)
        return file.to_dict() if file else None
    
    
    def get_symbol_details(self, project_name, symbol_id):
        project_ir = self.typed_ir_cache.load(project_name)
        symbol = project_ir.find_symbol(symbol_id)
        return symbol.to_dict() if symbol else None

    def get_file_source(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    
