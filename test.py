# test_ir.py
from services.project_service import ProjectService
from infrastructure.typed_ir_cache import TypedIRCache


class Service:
    def __init__(self, typed_ir_cache):
        self.project_ser = ProjectService(typed_ir_cache)

    def load_projects(self):
        return self.project_ser.get_existing_projects()
    
    def load_project(self, project_name):
        return self.project_ser.load_project(project_name)
        


if __name__ == "__main__":
    project_name = "project_scanner"

    cache = TypedIRCache("cache")
    service = Service(cache)
    service.load_projects()
    #service.load_project(project_name)
